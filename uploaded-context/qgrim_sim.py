"""qgrim_sim.py — pure-Python software model of the QGRIM core.

Mirrors the RTL bit-for-bit at the algorithmic level (Q4.12 fixed-point,
Born-rule measurement, paired addressing). Use it to verify programs
before flashing the FPGA.

Usage:
    python qgrim_sim.py examples/bell.qasm
"""

from __future__ import annotations
import math
import random
import sys
from dataclasses import dataclass, field
from pathlib import Path

from asm import assemble, PHASE_LUT, OPCODES

QUBITS = 4
STATES = 1 << QUBITS

# ---------- Q4.12 helpers (we keep math in float and only quantize on store) ----------
ONE_Q12 = 1 << 12


def quantize(x: float) -> float:
    """Round to Q4.12 grid, clamp to representable range."""
    q = round(x * ONE_Q12)
    q = max(-(1 << 15), min((1 << 15) - 1, q))
    return q / ONE_Q12


@dataclass
class QGRIMSim:
    seed: int = 0xACE1
    state: list[complex] = field(default_factory=lambda: [0j] * STATES)
    pc: int = 0
    halted: bool = False
    measurements: dict[int, int] = field(default_factory=dict)
    pi: float = 0.0
    trace: list[tuple[int, int, float]] = field(default_factory=list)

    def __post_init__(self):
        self.state[0] = 1.0 + 0j
        random.seed(self.seed)

    # ---- gates ----
    def init(self):
        self.state = [0j] * STATES
        self.state[0] = 1.0 + 0j

    def hadamard(self, q: int):
        new = self.state[:]
        mask = 1 << q
        for i in range(STATES):
            if i & mask:
                continue
            j = i | mask
            a, b = self.state[i], self.state[j]
            new[i] = quantize(((a + b) / math.sqrt(2)).real) + 1j * quantize(
                ((a + b) / math.sqrt(2)).imag
            )
            new[j] = quantize(((a - b) / math.sqrt(2)).real) + 1j * quantize(
                ((a - b) / math.sqrt(2)).imag
            )
        self.state = new

    def pauli_x(self, q: int):
        new = self.state[:]
        mask = 1 << q
        for i in range(STATES):
            if i & mask:
                continue
            j = i | mask
            new[i], new[j] = self.state[j], self.state[i]
        self.state = new

    def cnot(self, c: int, t: int):
        new = self.state[:]
        cmask, tmask = 1 << c, 1 << t
        for i in range(STATES):
            if i & tmask:
                continue
            if not (i & cmask):
                continue
            j = i | tmask
            new[i], new[j] = self.state[j], self.state[i]
        self.state = new

    def phase(self, q: int, idx: int):
        cos_v, sin_v = PHASE_LUT[idx & 0xF]
        cos_v = quantize(cos_v)
        sin_v = quantize(sin_v)
        factor = complex(cos_v, sin_v)
        mask = 1 << q
        for i in range(STATES):
            if i & mask:
                v = self.state[i] * factor
                self.state[i] = quantize(v.real) + 1j * quantize(v.imag)

    def swap(self, a: int, b: int):
        ma, mb = 1 << a, 1 << b
        new = self.state[:]
        for i in range(STATES):
            ba = bool(i & ma)
            bb = bool(i & mb)
            if ba == bb:
                continue
            j = i & ~ma & ~mb
            if ba:
                j |= mb
            if bb:
                j |= ma
            if j > i:
                new[i], new[j] = self.state[j], self.state[i]
        self.state = new

    def measure(self, q: int) -> int:
        mask = 1 << q
        p0 = sum(abs(a) ** 2 for i, a in enumerate(self.state) if not (i & mask))
        u = random.random()
        bit = 0 if u < p0 else 1
        keep = p0 if bit == 0 else (1.0 - p0)
        norm = math.sqrt(keep) if keep > 0 else 1.0
        new = []
        for i, a in enumerate(self.state):
            survives = ((i & mask) >> q) == bit
            if survives:
                v = a / norm
                new.append(quantize(v.real) + 1j * quantize(v.imag))
            else:
                new.append(0j)
        self.state = new
        self.measurements[q] = bit
        self.pi = quantize(self.pi + (16 / 4096))
        return bit

    # ---- program execution ----
    def step(self, instr: int) -> bool:
        op = (instr >> 12) & 0xF
        a = (instr >> 8) & 0xF
        b = (instr >> 4) & 0xF
        imm = instr & 0xF
        if op == 0x0:
            pass  # NOP
        elif op == 0x1:
            self.hadamard(a)
        elif op == 0x2:
            self.pauli_x(a)
        elif op == 0x3:
            self.cnot(a, b)
        elif op == 0x4:
            self.measure(a)
        elif op == 0x5:
            self.phase(a, imm)
        elif op == 0x6:
            self.init()
        elif op == 0x7:
            self.swap(a, b)
        elif op == 0x8:
            self.state = [0j] * STATES
            self.state[a] = 1.0 + 0j
        elif op == 0x9:
            self.trace.append(
                (self.pc, sum((b << k) for k, b in self.measurements.items()), self.pi)
            )
        elif op == 0xE:
            pass  # WAIT
        elif op == 0xF:
            self.halted = True
            return False
        else:
            raise RuntimeError(f"unknown opcode 0x{op:X} at pc={self.pc}")
        self.pc += 1
        return True

    def run(self, program: list[int], max_cycles: int = 10_000):
        self.pc = 0
        self.halted = False
        for _ in range(max_cycles):
            if self.pc >= len(program) or self.halted:
                break
            if not self.step(program[self.pc]):
                break

    # ---- helpers ----
    def dump(self):
        print("State vector:")
        for i, a in enumerate(self.state):
            if abs(a) > 1e-4:
                print(
                    f"  |{i:04b}>  {a.real:+.4f} {a.imag:+.4f}j   (P={abs(a) ** 2:.4f})"
                )
        if self.measurements:
            print("Measurements:", self.measurements)
        print(f"PI: {self.pi:.4f}")


def main():
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} program.qasm [seed]", file=sys.stderr)
        sys.exit(2)
    src = Path(sys.argv[1]).read_text()
    seed = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0xACE1
    program = assemble(src)
    sim = QGRIMSim(seed=seed)
    sim.run(program)
    sim.dump()


if __name__ == "__main__":
    main()

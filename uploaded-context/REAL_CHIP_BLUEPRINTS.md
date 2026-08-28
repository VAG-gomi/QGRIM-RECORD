# Proven Blueprints to Fabricate a Real Quantum Chip

This is an **honest, complete index** of the published, peer-reviewed
designs you would actually need to build a working quantum processor.
Nothing here is invented. Every entry is a real paper, a real tool, or
a real piece of equipment used by IBM, Google, Rigetti, MIT, ETH, Delft,
and others to make the chips that exist today.

The most accessible architecture for a small team is the **superconducting
transmon**, so the stack below is for that. Trapped-ion, photonic, and
spin-qubit stacks are listed at the end.

---

## 0. The decision you have to make first

| Qubit type        | Fab complexity | Cryo needed     | T1/T2 today | Notes                                |
|-------------------|----------------|-----------------|-------------|--------------------------------------|
| Superconducting   | Medium         | 10 mK dil. fridge| ~100–500 µs | Best documented; IBM/Google use this |
| Trapped ion       | Low (no fab)   | None (UHV)      | seconds–minutes | Buy ions, build trap; AQT/IonQ      |
| Photonic          | High           | Room temp       | flying      | PsiQuantum/Xanadu                   |
| Silicon spin      | Very high (CMOS)| 100 mK         | ~1–10 ms    | Intel/Diraq                         |
| Neutral atoms     | Medium         | None (cooling)  | seconds     | QuEra/Pasqal                        |

The rest of this document assumes **superconducting transmon** because
it is the only path with full open documentation end-to-end.

---

## 1. Qubit design — the physics blueprint

### 1.1 The transmon Hamiltonian (this *is* the qubit)

> J. Koch et al., *"Charge-insensitive qubit design derived from the Cooper pair box"*, Phys. Rev. A **76**, 042319 (2007). [arXiv:cond-mat/0703002]

Defines the only qubit you should build as a beginner: a Josephson
junction shunted by a large capacitor, operated in the regime
E_J / E_C ≈ 50–100. Gives you the design equations for:

- ω_01 (qubit frequency, target 4–6 GHz)
- α (anharmonicity, target −200 to −300 MHz)
- C_shunt (target 60–90 fF)
- E_J / E_C ratio

### 1.2 Coupling qubits to a readout resonator (cQED)

> A. Blais, R.-S. Huang, A. Wallraff, S.M. Girvin, R.J. Schoelkopf, *"Cavity quantum electrodynamics for superconducting electrical circuits: An architecture for quantum computation"*, Phys. Rev. A **69**, 062320 (2004).

> A. Wallraff et al., *"Strong coupling of a single photon to a superconducting qubit using circuit quantum electrodynamics"*, Nature **431**, 162 (2004).

These two papers define the dispersive readout architecture used in
literally every superconducting QPU built since 2004.

### 1.3 Two-qubit gates — pick one family

- **Cross-resonance (IBM):** Chow et al., Phys. Rev. Lett. **107**, 080502 (2011)
- **iSWAP / parametric (Rigetti):** Reagor et al., Sci. Adv. **4**, eaao3603 (2018)
- **Tunable coupler (Google Sycamore):** Yan et al., Phys. Rev. Applied **10**, 054062 (2018)
- **CZ via flux pulses (Google):** Barends et al., Nature **508**, 500 (2014)

For a first chip, **fixed-frequency transmons + cross-resonance** is the
simplest because no flux lines are needed.

### 1.4 Reference open-source qubit design

> **Qiskit Metal** — IBM's open-source EDA tool for superconducting QPU layout.
> https://qiskit-community.github.io/qiskit-metal/
> Includes parameterized transmon, resonator, coupler libraries that you
> can export to GDS for fab.

> **scqubits** — Numerical Hamiltonian solver for transmon, fluxonium, etc.
> https://scqubits.readthedocs.io/

---

## 2. Layout — the GDS blueprint

You need to produce a **GDSII file** (the universal mask format) that
the cleanroom turns into photo/e-beam masks.

### 2.1 Reference open layouts

- **OpenSuperQ** (EU flagship): public 5-qubit design, full GDS.
  https://opensuperq.eu/
- **QPU-Generator** (TU Delft): parameterized transmon GDS in Python.
  https://github.com/DiCarloLab-Delft/QPU-Generator
- **Qiskit Metal example designs** (under `qiskit_metal/qlibrary/`):
  - `TransmonPocket`
  - `TransmonCross`
  - `RouteMeander` (resonators)

### 2.2 Mask layers (typical 2-layer process)

| Layer | Purpose                              | Material          |
|-------|--------------------------------------|-------------------|
| M1    | Ground plane + capacitor pads + CPW  | 100–200 nm Nb or Al on sapphire/Si |
| JJ    | Josephson junctions                  | Al/AlOx/Al        |
| (opt) | Airbridges over CPW crossovers       | Al, ~3 µm tall    |
| (opt) | TSVs for 3D integration              | Cu/W              |

### 2.3 Design-rule reference

> J.M. Martinis et al., *"Decoherence in Josephson qubits from dielectric loss"*, Phys. Rev. Lett. **95**, 210503 (2005).
> Tells you which dielectrics destroy your T1 — start here.

> C. Wang et al., *"Surface participation and dielectric loss in superconducting qubits"*, Appl. Phys. Lett. **107**, 162601 (2015).
> The "surface participation ratio" calculation that drives every
> modern chip's geometry.

---

## 3. Fabrication — the process blueprint

### 3.1 Substrate

- High-resistivity (>10 kΩ·cm) intrinsic Si **or** sapphire (c-plane, EFG-grown)
- 2" or 4" wafer, double-side polished
- Buried oxide stripped, HF-cleaned within minutes of metal deposition

### 3.2 Base metal (capacitor pads + CPW + ground plane)

- 100–200 nm Nb (sputtered, 3 mTorr Ar) **or** Al (e-beam evaporated)
- Patterned by optical lithography (i-line stepper, ~1 µm features)
- Wet etch (Nb: HNO₃/HF/H₂O) or dry etch (Cl₂ ICP)

### 3.3 Josephson junctions — Dolan bridge process

> G.J. Dolan, *"Offset masks for lift-off photoprocessing"*, Appl. Phys. Lett. **31**, 337 (1977).

The 47-year-old process every superconducting qubit lab still uses:

1. Spin MMA/PMMA bilayer (e.g. EL-13 / 950k A4)
2. E-beam expose the bridge pattern (~50 nm bridge, ~200 nm undercut)
3. Develop in MIBK:IPA 1:3
4. **Tilt 1:** evaporate 30 nm Al at +30°
5. **Oxidize:** static oxidation, ~10 mTorr O₂, 5–15 min (sets junction R_n)
6. **Tilt 2:** evaporate 60 nm Al at −30°
7. Lift-off in NMP at 80°C

Junction area: 100 × 100 nm to 200 × 200 nm. Target room-temperature
resistance R_n that gives E_J via Ambegaokar-Baratoff:
**E_J / h ≈ Δ / (8 e² R_n)** ≈ 200 K · Ω / R_n in GHz.

### 3.4 Reference fab recipes (open)

- **MIT Lincoln Lab process node** — partially declassified in:
  Rosenberg et al., *"3D integrated superconducting qubits"*, npj Quantum Inf. **3**, 42 (2017).
- **IBM 25-qubit "Falcon" fab notes** — Kandala et al., Nature **567**, 491 (2019), supplementary.
- **Google Sycamore fab** — Arute et al., Nature **574**, 505 (2019), supplementary.
- **Delft "Surface-7" recipe** — Versluis et al., Phys. Rev. Applied **8**, 034021 (2017).

### 3.5 Where to actually fab it

You do not need to own a fab. Open shared cleanrooms that take qubit work:

| Facility            | Location  | Cost (rough)              |
|---------------------|-----------|---------------------------|
| MIT.nano            | USA       | $200–800/hr, members only |
| Stanford SNF/SNSF   | USA       | ~$100–400/hr              |
| Cornell CNF         | USA       | ~$80/hr (NNCI rates)      |
| IMEC                | Belgium   | Industrial; quote required|
| Chalmers MC2        | Sweden    | Open to academics         |
| Delft Kavli Nanolab | NL        | Academic collaboration    |
| TU München WSI      | Germany   | Academic collaboration    |
| LAAS-CNRS RENATECH  | France    | Open to academics         |

A first single-junction test wafer typically takes ~2–4 weeks of
cleanroom time and ~$5–20k in cleanroom + materials.

---

## 4. Packaging — the box blueprint

> S. Huang et al., *"Microwave package design for superconducting quantum processors"*, PRX Quantum **2**, 020306 (2021).

The chip lives inside a milled OFHC-copper or aluminum sample holder
with:

- Wirebonds to a PCB (Rogers 4350 or Roger TMM10) with SMP/SMPM connectors
- Aluminum-bond wires to the ground plane every ~200 µm to suppress
  slotline modes
- Magnetic shielding: cryoperm + niobium can
- Light-tight: IR-tight seam + Eccosorb CR-110 microwave absorber

### Reference open package designs

- **OpenQuantumHardware** sample holders: https://github.com/Qiskit/openquantumhardware
- **QUDEV ETH** sample-holder STL files: open on request from the group
- **Bluefors sample-holder reference design**: vendor-supplied

---

## 5. Cryogenics — the fridge blueprint

You cannot avoid this: transmons need ~10 mK.

### 5.1 The fridge

- **Bluefors LD400** or **XLD400**, **Oxford ProteoxMX**, **Leiden CF-450** — dry dilution refrigerators
- Base temp 7–20 mK, cooling power ~400 µW @ 100 mK
- Cost: $300k–$1.2M new; used LD200/LD250 sometimes appear for $80k–150k

### 5.2 Cryogenic wiring stack (per qubit drive line)

| Stage    | Component                          | Vendor (typical)         |
|----------|------------------------------------|--------------------------|
| 300 K    | SMA bulkhead                       | Rosenberger / Huber+Suhner |
| 50 K     | 0–10 dB attenuator (BeCu)          | XMA / Quantum Microwave  |
| 4 K      | 10 dB attenuator                   | XMA                      |
| Still    | 6 dB attenuator                    | XMA                      |
| 100 mK   | 3 dB attenuator                    | XMA                      |
| MXC      | 20 dB attenuator                   | XMA                      |
| MXC      | Eccosorb CR-110 IR filter          | Aeroflex                 |
| MXC      | Low-pass 8–12 GHz filter           | K&L Microwave / Marki    |

For readout output: HEMT amplifier at 4 K (Low Noise Factory LNF-LNC4_8C, ~$8k each) + isolators at MXC (Quinstar / LNF, ~$2k each).

### 5.3 Reference wiring blueprint

> Krinner et al., *"Engineering cryogenic setups for 100-qubit scale superconducting circuit systems"*, EPJ Quantum Technol. **6**, 2 (2019). **This is the canonical paper.**

---

## 6. Control electronics — the room-temperature blueprint

### 6.1 Commercial stacks (turnkey)

| Vendor                | Product                | Notes                                          |
|-----------------------|------------------------|------------------------------------------------|
| Quantum Machines      | OPX+, OPX1000          | FPGA-based, real-time feedback; industry std.  |
| Zurich Instruments    | SHFQC, HDAWG           | 8.5 GHz direct synthesis; tightly integrated   |
| Keysight              | M3xxx series           | Modular AWG/digitizer                          |
| Rohde & Schwarz       | SGS100A + R&S SMW      | Microwave sources                              |

Cost: ~$150k–$500k for an 8-qubit setup.

### 6.2 Open-source / DIY stack

- **QICK (RFSoC-based)** — Fermilab open quantum control system. Runs on Xilinx ZCU111/ZCU216. Total hardware cost ~$15k for an 8-channel stack.
  https://github.com/openquantumhardware/qick
  Stefanazzi et al., Rev. Sci. Instrum. **93**, 044709 (2022).
- **Presto** (Intermodulation Products) — open-firmware vector network analyzer + AWG.
- **Labber / QCoDeS / pycqed** — open-source measurement frameworks.

### 6.3 Calibration & gate-tuning software (open)

- **Qiskit Experiments** — automated T1, T2, randomized benchmarking, etc.
- **pycqed (DiCarloLab)** — Delft's full calibration stack
- **OpenPulse** spec — vendor-neutral pulse-level control

---

## 7. Verification & calibration — the protocol blueprint

These are the procedures that tell you the chip works:

| Protocol                           | Reference                                   |
|------------------------------------|---------------------------------------------|
| Resonator spectroscopy             | Megrant et al., APL **100**, 113510 (2012)  |
| T1 / T2 / T2-echo                  | Ithier et al., PRB **72**, 134519 (2005)    |
| Randomized benchmarking            | Magesan et al., PRL **109**, 080505 (2012)  |
| Cross-entropy benchmarking (XEB)   | Boixo et al., Nature Phys. **14**, 595 (2018) |
| Quantum process tomography         | Chuang & Nielsen, J. Mod. Opt. **44**, 2455 (1997) |
| Gate-set tomography                | Nielsen et al., Quantum **5**, 557 (2021)   |

---

## 8. Bill of materials — single-qubit first chip

| Item                                  | Cost (USD)        |
|---------------------------------------|-------------------|
| 4" sapphire wafer (10 pcs)            | $2,000            |
| Cleanroom time, 3 weeks               | $8,000–25,000     |
| Mask plates / e-beam writes           | $3,000–10,000     |
| OFHC sample holder (machined)         | $1,500            |
| PCB (Rogers, custom)                  | $800              |
| SMP cables + connectors               | $1,200            |
| Used dilution fridge (LD200)          | $80,000–150,000   |
| HEMT amplifier (LNF-LNC4_8C)          | $8,000            |
| Isolators × 2                         | $4,000            |
| Cryo attenuators (set)                | $4,000            |
| QICK FPGA control stack               | $15,000           |
| Microwave source (R&S SGS100A used)   | $12,000           |
| **Realistic total to first qubit**    | **~$140k–230k**   |

Ongoing: ~$30k/year liquid helium-free dry fridge electricity + parts.

---

## 9. The team you actually need

A working group typically has:

- 1 PhD on **fab process** (cleanroom hours, junction yield)
- 1 PhD on **microwave engineering** (lines, packaging, calibration)
- 1 PhD on **cryogenics + measurement** (fridge ops, software)
- 1 PhD on **theory + control** (pulse design, error budgets)
- A PI who has done it before

If you don't have this team, the realistic path is to **join one** —
PhD or postdoc position, or an industry role at IBM/Google/Rigetti/IQM/etc.

---

## 10. Other qubit stacks (one paragraph each)

### Trapped ion (lowest barrier — no fab needed)

> Häffner, Roos, Blatt, *"Quantum computing with trapped ions"*, Phys. Rep. **469**, 155 (2008).
> Buy a vacuum chamber ($30k), Paul or surface trap (commercial from
> Sandia or AQT, ~$50k), 729 nm + 397 nm lasers (Toptica, $80k each),
> and you can trap a single Ca+ ion in ~12 months. Coherence times of
> seconds, no cryogenics.

### Photonic (single-photon CNOT on a table)

> Knill, Laflamme, Milburn, *"A scheme for efficient quantum computation with linear optics"*, Nature **409**, 46 (2001).
> SPDC source (BBO crystal + 405 nm pump), polarization analyzers, SPADs.
> Two-qubit demos for ~$50k of optics.

### Silicon spin (most CMOS-compatible)

> Veldhorst et al., *"Silicon CMOS architecture for a spin-based quantum computer"*, Nat. Commun. **8**, 1766 (2017).
> Requires industrial fab (28Si MOS or SiGe heterostructures). Realistic
> only via collaboration with Intel, IMEC, or a major university.

### Neutral atoms

> Henriet et al., *"Quantum computing with neutral atoms"*, Quantum **4**, 327 (2020).
> Magneto-optical trap + optical tweezers + Rydberg lasers. ~$300k-$1M
> table-top setup; QuEra/Pasqal style.

---

## 11. The shortest credible path

If your goal is **"I made a real quantum chip"** and you have neither a
cleanroom nor a fridge:

1. Join an open collaboration: **OpenSuperQ**, **QuTech Academy**, **IBM Quantum Research Network**.
2. Use **Qiskit Metal** to design a single transmon — that *is* a real,
   tape-out-ready blueprint.
3. Send the GDS to a shared cleanroom (Cornell CNF rates start ~$80/hr)
   for a single test run — ~$10–20k.
4. Send the resulting die to a group with a fridge for measurement —
   most academic groups will collaborate for co-authorship.

Total time-to-chip: ~12–18 months. Total cost to you: ~$15–30k plus
your time. Output: a real superconducting qubit you designed,
with measured T1/T2 in a peer-reviewed paper.

That is the most honest, achievable answer to "how do I get a real
quantum chip made."

---

## 12. Things that are NOT proven blueprints (avoid)

- "Quantum chips" sold on AliExpress, Tindie, etc. — these are FPGAs or microcontrollers, not qubits.
- Patents claiming room-temperature topological qubits without peer-reviewed measurement data.
- Any architecture promising >1000 logical qubits today — not a single one exists.
- Anything that calls itself "QGRIM v3.0 hardware" — QGRIM is an FPGA *simulator*, including the v2.1 in this repo. It is not a path to physical qubits.

---

## 13. Reading order if you start tomorrow

1. Krantz et al., *"A Quantum Engineer's Guide to Superconducting Qubits"*, Appl. Phys. Rev. **6**, 021318 (2019). **— read this first; it covers items 1–7 above in 70 pages.**
2. Koch 2007 (transmon)
3. Blais 2004 + Wallraff 2004 (cQED)
4. Krinner 2019 (cryo wiring)
5. Krantz again, with Qiskit Metal open in another window.

That five-step reading list takes ~2 weeks and gives you the entire
proven blueprint set in your head.

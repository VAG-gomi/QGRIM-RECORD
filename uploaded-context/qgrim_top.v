// qgrim_top.v — QGRIM v2.1 top level
// Wires SPI ↔ register file ↔ instruction decoder ↔ gate engines ↔ state vector.
`timescale 1ns / 1ps
`default_nettype none

module qgrim_top (
    input  wire       clk_in,    // unused if SB_HFOSC instantiated
    input  wire       rst_n,
    // SPI
    input  wire       sclk,
    input  wire       mosi,
    output wire       miso,
    input  wire       ss_n,
    // Status
    output wire       irq,
    output wire [7:0] led
);

    // ---------------- clocks ----------------
    wire clk_hf, clk_sys;
    osc        u_osc        (.clk(clk_hf));
    clock_div #(.DIV(4)) u_div (.clk_in(clk_hf), .rst_n(rst_n), .clk_out(clk_sys));

    // ---------------- SPI ↔ register bus ----------------
    wire        spi_packet_done;
    wire [7:0]  spi_addr;
    wire [31:0] spi_wdata;
    wire        spi_we;
    wire [31:0] spi_rdata;

    spi_slave u_spi (
        .clk(clk_sys), .rst_n(rst_n),
        .sclk(sclk), .mosi(mosi), .miso(miso), .ss_n(ss_n),
        .addr_o(spi_addr), .wdata_o(spi_wdata),
        .we_o(spi_we), .rdata_i(spi_rdata),
        .packet_done_o(spi_packet_done)
    );

    // ---------------- program memory + bridge (FIX #1) ----------------
    wire        pgm_we;
    wire [7:0]  pgm_waddr;
    wire [15:0] pgm_wdata;
    wire [7:0]  pgm_raddr;
    wire [15:0] pgm_rdata;

    spi_bram_bridge u_pgm_bridge (
        .clk(clk_sys), .rst_n(rst_n),
        .spi_addr(spi_addr), .spi_wdata(spi_wdata),
        .spi_we(spi_we), .spi_packet_done(spi_packet_done),
        .pgm_we(pgm_we), .pgm_waddr(pgm_waddr), .pgm_wdata(pgm_wdata)
    );

    pgm_mem u_pgm (
        .clk(clk_sys),
        .we(pgm_we), .waddr(pgm_waddr), .wdata(pgm_wdata),
        .raddr(pgm_raddr), .rdata(pgm_rdata)
    );

    // ---------------- state vector RF ----------------
    // Arbitrated between gate engines and SPI direct access.
    wire        rf_we;
    wire [3:0]  rf_waddr;
    wire [31:0] rf_wdata;
    wire [3:0]  rf_raddr_a, rf_raddr_b;
    wire [31:0] rf_rdata_a, rf_rdata_b;

    state_vector_rf #(.QUBITS(4)) u_rf (
        .clk(clk_sys), .rst_n(rst_n),
        .we(rf_we), .waddr(rf_waddr), .wdata(rf_wdata),
        .raddr_a(rf_raddr_a), .raddr_b(rf_raddr_b),
        .rdata_a(rf_rdata_a), .rdata_b(rf_rdata_b)
    );

    // ---------------- decoder + gates ----------------
    wire [15:0] pi_value;
    wire [3:0]  meas_basis;
    wire        meas_valid;
    wire        busy, done, error_flag;
    wire [7:0]  pc_value;

    instr_decoder u_dec (
        .clk(clk_sys), .rst_n(rst_n),
        .start(spi_we && spi_addr == 8'h00 && spi_wdata[0]),
        .core_reset(spi_we && spi_addr == 8'h00 && spi_wdata[1]),
        .pgm_raddr(pgm_raddr), .pgm_rdata(pgm_rdata),
        .rf_we(rf_we), .rf_waddr(rf_waddr), .rf_wdata(rf_wdata),
        .rf_raddr_a(rf_raddr_a), .rf_raddr_b(rf_raddr_b),
        .rf_rdata_a(rf_rdata_a), .rf_rdata_b(rf_rdata_b),
        .pi_value(pi_value),
        .meas_basis(meas_basis), .meas_valid(meas_valid),
        .pc_o(pc_value),
        .busy_o(busy), .done_o(done), .error_o(error_flag)
    );

    // ---------------- status ----------------
    assign irq = done | meas_valid;
    assign led = pi_value[15:8];   // visible heartbeat

    // SPI read mux
    reg [31:0] spi_rdata_r;
    always @(*) begin
        case (spi_addr)
            8'h08:   spi_rdata_r = {16'h0, pi_value};
            8'h0C:   spi_rdata_r = {27'h0, meas_valid, meas_basis};
            8'h10:   spi_rdata_r = {29'h0, error_flag, done, busy};
            8'h14:   spi_rdata_r = {24'h0, pc_value};
            8'h1C:   spi_rdata_r = 32'h0000_0210;
            default: spi_rdata_r = 32'h0;
        endcase
    end
    assign spi_rdata = spi_rdata_r;

endmodule
`default_nettype wire

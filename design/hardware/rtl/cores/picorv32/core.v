// Adapter module to connect picorv32 to universal testbench
module core (
    input clk,
    input rst_n,
    // Instruction memory interface
    output [31:0] imem_addr,
    input [31:0] imem_data,
    output imem_en,
    // Data memory interface
    output [31:0] dmem_addr,
    output [31:0] dmem_wdata,
    input [31:0] dmem_rdata,
    output dmem_en,
    output dmem_we,
    // Debug interface
    output [31:0] debug_pc,
    output [31:0] debug_instr,
    output [4:0] debug_rd,
    output [31:0] debug_rd_wdata,
    output debug_rd_we
);

    // Internal signals
    wire trap;
    wire mem_valid;
    wire mem_instr;
    wire mem_ready;
    wire [31:0] mem_addr;
    wire [31:0] mem_wdata;
    wire [3:0] mem_wstrb;
    wire [31:0] mem_rdata;

    // Reset signal conversion (active low to active high)
    wire reset = ~rst_n;

    // Instruction memory access signals
    assign imem_addr = mem_instr ? mem_addr : 32'b0;
    assign imem_en = mem_instr & mem_valid;

    // Data memory access signals
    assign dmem_addr = !mem_instr ? mem_addr : 32'b0;
    assign dmem_wdata = mem_wdata;
    assign dmem_en = !mem_instr & mem_valid;
    assign dmem_we = |mem_wstrb;

    // Memory ready signal (always ready for simplicity)
    assign mem_ready = 1'b1;

    // Combine instruction and data memory read data
    assign mem_rdata = mem_instr ? imem_data : dmem_rdata;

    // Debug interface (connected to minimal outputs for now)
    assign debug_pc = mem_addr;  // Approximate PC (when fetching instruction)
    assign debug_instr = imem_data;  // Current instruction
    assign debug_rd = 5'b0;  // Not directly available from picorv32 interface
    assign debug_rd_wdata = 32'b0;  // Not directly available
    assign debug_rd_we = 1'b0;  // Not directly available

    // Instantiate the picorv32 core
    picorv32 #(
        .ENABLE_COUNTERS(1),
        .ENABLE_REGS_16_31(1),
        .ENABLE_REGS_DUALPORT(1),
        .PROGADDR_RESET(32'h00000000),
        .STACKADDR(32'h00010000)
    ) picorv32_core (
        .clk(clk),
        .resetn(rst_n),
        .trap(trap),
        .mem_valid(mem_valid),
        .mem_instr(mem_instr),
        .mem_ready(mem_ready),
        .mem_addr(mem_addr),
        .mem_wdata(mem_wdata),
        .mem_wstrb(mem_wstrb),
        .mem_rdata(mem_rdata)
    );

endmodule

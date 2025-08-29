#!/bin/bash
# Script to run the simple_core with hello-world using Bazel

# Clean build artifacts
echo "Cleaning previous build artifacts..."
bazel clean

# Compile the hello-world program for simple_core
echo "Building hello-world for simple_core..."
bazel build --config=simple_core //design/software/hello-world:executable

# Get the path to the generated hex file
HEX_FILE="$(bazel info bazel-bin)/design/software/hello-world/hello_world.hex"
echo "Generated hex file: $HEX_FILE"

# Create output directory
mkdir -p output

# Copy the hex file to a more accessible location
cp "$HEX_FILE" output/hello_world.hex
echo "Copied hex file to output/hello_world.hex"

# Create a simple Verilog testbench for simulation
cat > output/simple_tb.v << 'EOL'
`timescale 1ns / 1ps

module testbench;
    // Clock and reset generation
    reg clk = 0;
    reg rst_n = 0;
    
    // Always toggle clock
    always #5 clk = ~clk;
    
    // Wires to connect to the core
    wire [31:0] imem_addr;
    reg [31:0] imem_data;
    wire imem_en;
    wire [31:0] dmem_addr;
    wire [31:0] dmem_wdata;
    reg [31:0] dmem_rdata;
    wire dmem_en;
    wire dmem_we;
    wire [31:0] debug_pc;
    wire [31:0] debug_instr;
    wire [4:0] debug_rd;
    wire [31:0] debug_rd_wdata;
    wire debug_rd_we;
    
    // Memory array
    reg [31:0] imem [0:4095];
    reg [31:0] dmem [0:4095];
    integer i;
    
    // Core instance
    core dut (
        .clk(clk),
        .rst_n(rst_n),
        .imem_addr(imem_addr),
        .imem_data(imem_data),
        .imem_en(imem_en),
        .dmem_addr(dmem_addr),
        .dmem_wdata(dmem_wdata),
        .dmem_rdata(dmem_rdata),
        .dmem_en(dmem_en),
        .dmem_we(dmem_we),
        .debug_pc(debug_pc),
        .debug_instr(debug_instr),
        .debug_rd(debug_rd),
        .debug_rd_wdata(debug_rd_wdata),
        .debug_rd_we(debug_rd_we)
    );
    
    // Memory read
    always @(*) begin
        if (imem_en) begin
            imem_data = imem[imem_addr[13:2]];
        end else begin
            imem_data = 32'h0;
        end
    end
    
    // Data memory read/write
    always @(posedge clk) begin
        if (dmem_en) begin
            if (dmem_we) begin
                dmem[dmem_addr[13:2]] <= dmem_wdata;
            end
            dmem_rdata <= dmem[dmem_addr[13:2]];
        end
    end
    
    // Load program and run simulation
    initial begin
        // Clear memory
        for (i = 0; i < 4096; i = i + 1) begin
            imem[i] = 32'h0;
            dmem[i] = 32'h0;
        end
        
        // Load hex file (relative to the run directory)
        $display("Loading program from hello_world.hex");
        $readmemh("hello_world.hex", imem);
        
        // Reset sequence
        rst_n = 0;
        #20 rst_n = 1;
        
        // Run for a while
        #10000;
        
        // End simulation
        $display("Simulation finished");
        $finish;
    end
    
    // Monitor execution
    always @(posedge clk) begin
        if (rst_n) begin
            $display("PC: %h, INSTR: %h", debug_pc, debug_instr);
            if (debug_rd_we && debug_rd != 0) begin
                $display("  x%0d <= %h", debug_rd, debug_rd_wdata);
            end
        end
    end
endmodule
EOL

# Run the simulation
echo "Running simulation..."
cd output
iverilog -o sim_core ../design/hardware/rtl/cores/simple_core/simple_core.v simple_tb.v
vvp sim_core

echo "Simulation completed!"

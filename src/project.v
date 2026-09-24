/*
 * Copyright (c) 2026 Elisa
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // All output pins must be assigned. If not used, assign to 0.
  //assign uo_out  = ui_in + uio_in;  // Example: ou_out is the sum of ui_in and uio_in
  //assign uio_out = 0;
  //assign uio_oe  = 0;
  
  // Give the control inputs readable names
  wire en   = ui_in[0];  // 1 = count up
  wire load = ui_in[1];  // 1 = load a new value on the next clock edge
  wire oe   = ui_in[2];  // 1 = drive the count out on uio[7:0], 0 = high-Z

  reg[7:0] count;

  always @(posedge clk) begin
    if (!rst_n)
      count <= 8'd0;  // reset to 0
    else if (load)
      count <= uio_in;            // synchronous load (only on a clock edge)
    else if (en)
      count <= count + 8'd1;      // count up
  end

  assign uio_out = count;
  assign uio_oe  = {8{oe}};
  assign uo_out  = count;

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, ui_in[7:1], uio_in, 1'b0};

endmodule

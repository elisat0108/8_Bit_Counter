# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge, Timer

# Control bits on ui_in
EN = 0b001
LOAD = 0b010
OE = 0b100
 

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1
    assert dut.uo_out.value == 0, "count should be 0 after reset"

    dut._log.info("Count up")
    dut.ui_in.value = EN
    await ClockCycles(dut.clk, 5)
    await FallingEdge(dut.clk)
    assert dut.uo_out.value == 5, "should count to 5"

    dut._log.info("Hold")
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 5)
    await FallingEdge(dut.clk)
    assert dut.uo_out.value == 5, "should hold at 5 when EN = 0"

    dut._log.info("Synchronous load")
    dut.uio_in.value = 200
    dut.ui_in.value = LOAD
    await Timer(1, unit="us")  # still before the next rising edge
    assert dut.uo_out.value == 5, "load must wait for the clock edge"
    await FallingEdge(dut.clk)  # a rising edge has now happened
    assert dut.uo_out.value == 200, "should load 200 on the clock edge"
 
    dut._log.info("Wraparound")
    dut.uio_in.value = 254
    await FallingEdge(dut.clk)
    assert dut.uo_out.value == 254
    dut.ui_in.value = EN
    await ClockCycles(dut.clk, 3)
    await FallingEdge(dut.clk)
    assert dut.uo_out.value == 1, "should wrap 255 -> 0 -> 1"
 
    # ---- Tri-state outputs ----
    dut._log.info("Tri-state outputs")
    dut.ui_in.value = 0  # OE off
    await Timer(1, unit="us")
    assert dut.uio_oe.value == 0x00, "uio pins should be high-Z when OE = 0"
    dut.ui_in.value = OE  # OE on
    await Timer(1, unit="us")
    assert dut.uio_oe.value == 0xFF, "uio pins should drive when OE = 1"
    assert dut.uio_out.value == 1, "uio pins should show the count"
 
    # ---- Reset while counting ----
    # Note: this design uses a synchronous reset (rst_n is only sampled on
    # posedge clk), so pulling rst_n low does not clear count until the
    # next rising edge.
    dut._log.info("Reset while counting")
    dut.ui_in.value = EN
    await ClockCycles(dut.clk, 3)
    await FallingEdge(dut.clk)
    assert dut.uo_out.value == 4
    await Timer(1, unit="us")  # middle of the clock cycle, no rising edge
    dut.rst_n.value = 0
    await Timer(1, unit="ns")
    assert dut.uo_out.value == 4, "count should not clear before the next clock edge"
    await FallingEdge(dut.clk)  # a rising edge has now happened with rst_n low
    assert dut.uo_out.value == 0, "reset should clear the count on the clock edge"
 
    dut._log.info("All tests passed")
 

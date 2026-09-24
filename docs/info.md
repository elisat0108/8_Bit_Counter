<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This project is an 8-bit up counter with an enable input.

On each rising edge of the clock, the counter checks two things:

- If `rst_n` is low, the count resets to 0.
- Otherwise, if `ui[0]` (EN) is high, the count increases by 1.

If EN is low, the count holds its current value. The current count is always shown in binary on the output pins `uo[7:0]`, with `uo[0]` as the least significant bit. Since the counter is 8 bits wide, it counts from 0 to 255 and then wraps back to 0.

## How to test

1. Pull `rst_n` low for at least one clock cycle to reset the counter to 0.
2. Release reset by setting `rst_n` high.
3. Set `ui[0]` (EN) high. The value on `uo[7:0]` should increase by 1 on every clock cycle (0, 1, 2, 3, ...).
4. Set `ui[0]` low. The count should stop and hold its value.

## External hardware

None.
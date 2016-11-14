set_instance_assignment -name IO_STANDARD LVDS -to tmds[3]
set_location_assignment PIN_N15 -to tmds[3]
set_location_assignment PIN_N16 -to "tmds[3](n)"
set_instance_assignment -name IO_STANDARD LVDS -to tmds[2]
set_location_assignment PIN_R16 -to tmds[2]
set_location_assignment PIN_P16 -to "tmds[2](n)"
set_location_assignment PIN_R8 -to clock_50
set_instance_assignment -name IO_STANDARD LVDS -to tmds[1]
set_location_assignment PIN_L15 -to tmds[1]
set_location_assignment PIN_L16 -to "tmds[1](n)"
set_instance_assignment -name IO_STANDARD LVDS -to tmds[0]
set_location_assignment PIN_K15 -to tmds[0]
set_location_assignment PIN_K16 -to "tmds[0](n)"
set_instance_assignment -name PARTITION_HIERARCHY root_partition -to | -section_id Top
set_instance_assignment -name IO_STANDARD LVDS -to tmds[4]
set_location_assignment PIN_T10 -to tmds[4]
set_location_assignment PIN_R10 -to "tmds[4](n)"
set_instance_assignment -name IO_STANDARD LVDS -to tmds[5]
set_location_assignment PIN_J15 -to KEY[0]
set_location_assignment PIN_E1 -to KEY[1]

set_location_assignment PIN_G15 -to tmds[5]
set_location_assignment PIN_G16 -to "tmds[5](n)"
set_location_assignment PIN_P2 -to DRAM_ADDR[0]
set_location_assignment PIN_L4 -to DRAM_ADDR[12]
set_location_assignment PIN_N1 -to DRAM_ADDR[11]
set_location_assignment PIN_N2 -to DRAM_ADDR[10]
set_location_assignment PIN_P1 -to DRAM_ADDR[9]
set_location_assignment PIN_R1 -to DRAM_ADDR[8]
set_location_assignment PIN_T6 -to DRAM_ADDR[7]
set_location_assignment PIN_N8 -to DRAM_ADDR[6]
set_location_assignment PIN_T7 -to DRAM_ADDR[5]
set_location_assignment PIN_P8 -to DRAM_ADDR[4]
set_location_assignment PIN_M8 -to DRAM_ADDR[3]
set_location_assignment PIN_N6 -to DRAM_ADDR[2]
set_location_assignment PIN_N5 -to DRAM_ADDR[1]
set_location_assignment PIN_M6 -to DRAM_BA[1]
set_location_assignment PIN_M7 -to DRAM_BA[0]
set_location_assignment PIN_L1 -to DRAM_CAS_N
set_location_assignment PIN_L7 -to DRAM_CKE
set_location_assignment PIN_R4 -to DRAM_CLK
set_location_assignment PIN_P6 -to DRAM_CS_N
set_location_assignment PIN_K1 -to DRAM_DQ[15]
set_location_assignment PIN_N3 -to DRAM_DQ[14]
set_location_assignment PIN_P3 -to DRAM_DQ[13]
set_location_assignment PIN_R5 -to DRAM_DQ[12]
set_location_assignment PIN_R3 -to DRAM_DQ[11]
set_location_assignment PIN_T3 -to DRAM_DQ[10]
set_location_assignment PIN_T2 -to DRAM_DQ[9]
set_location_assignment PIN_T4 -to DRAM_DQ[8]
set_location_assignment PIN_R7 -to DRAM_DQ[7]
set_location_assignment PIN_J1 -to DRAM_DQ[6]
set_location_assignment PIN_J2 -to DRAM_DQ[5]
set_location_assignment PIN_K2 -to DRAM_DQ[4]
set_location_assignment PIN_K5 -to DRAM_DQ[3]
set_location_assignment PIN_L8 -to DRAM_DQ[2]
set_location_assignment PIN_G1 -to DRAM_DQ[1]
set_location_assignment PIN_G2 -to DRAM_DQ[0]
set_location_assignment PIN_T5 -to DRAM_DQM[1]
set_location_assignment PIN_R6 -to DRAM_DQM[0]
set_location_assignment PIN_L2 -to DRAM_RAS_N
set_location_assignment PIN_C2 -to DRAM_WE_N

set_location_assignment PIN_F2 -to ACC_CLK
set_location_assignment PIN_F1 -to ACC_DATA
set_location_assignment PIN_G5 -to ACC_SELECT
set_location_assignment PIN_M2 -to ACC_INTERRUPT


set_location_assignment PIN_M15 -to DIP[3]
set_location_assignment PIN_B9 -to DIP[2]
set_location_assignment PIN_T8 -to DIP[1]
set_location_assignment PIN_M1 -to DIP[0]

set_location_assignment PIN_A15 -to LED[0]
set_location_assignment PIN_A13 -to LED[1]
set_location_assignment PIN_B13 -to LED[2]
set_location_assignment PIN_A11 -to LED[3]
set_location_assignment PIN_D1 -to LED[4]
set_location_assignment PIN_F3 -to LED[5]
set_location_assignment PIN_B1 -to LED[6]
set_location_assignment PIN_L3 -to LED[7]

set_location_assignment PIN_A10 -to ADC_CS_N
set_location_assignment PIN_B10 -to ADC_SADDR
set_location_assignment PIN_A9 -to ADC_SDAT
set_location_assignment PIN_B14 -to ADC_SCLK

set_instance_assignment -name IO_STANDARD LVDS -to tmds[6]
set_location_assignment PIN_R9 -to tmds[6]
set_location_assignment PIN_T9 -to "tmds[6](n)"
set_instance_assignment -name IO_STANDARD LVDS -to tmds[7]
set_location_assignment PIN_R11 -to tmds[7]
set_location_assignment PIN_T11 -to "tmds[7](n)"
set_instance_assignment -name IO_STANDARD LVDS -to tmds[8]
set_location_assignment PIN_R12 -to tmds[8]
set_location_assignment PIN_T12 -to "tmds[8](n)"
set_instance_assignment -name IO_STANDARD LVDS -to tmds[9]
set_location_assignment PIN_R13 -to tmds[9]
set_location_assignment PIN_T13 -to "tmds[9](n)"
set_instance_assignment -name IO_STANDARD LVDS -to tmds[10]
set_location_assignment PIN_T14 -to tmds[10]
set_location_assignment PIN_T15 -to "tmds[10](n)"
set_instance_assignment -name IO_STANDARD LVDS -to tmds[11]
set_location_assignment PIN_F15 -to tmds[11]
set_location_assignment PIN_F16 -to "tmds[11](n)"
set_instance_assignment -name IO_STANDARD LVDS -to tmds[12]
set_location_assignment PIN_A3 -to tmds[12]
set_location_assignment PIN_A2 -to "tmds[12](n)"
set_instance_assignment -name IO_STANDARD LVDS -to tmds[13]
set_location_assignment PIN_B4 -to tmds[13]
set_location_assignment PIN_A4 -to "tmds[13](n)"
set_instance_assignment -name IO_STANDARD LVDS -to tmds[14]
set_location_assignment PIN_B5 -to tmds[14]
set_location_assignment PIN_A5 -to "tmds[14](n)"
set_instance_assignment -name IO_STANDARD LVDS -to tmds[15]
set_location_assignment PIN_B6 -to tmds[15]
set_location_assignment PIN_A6 -to "tmds[15](n)"

set_instance_assignment -name IO_STANDARD LVDS -to tmds[23]
set_location_assignment PIN_B8 -to tmds[23]
set_location_assignment PIN_A8 -to "tmds[23](n)"

set_instance_assignment -name IO_STANDARD LVDS -to tmds[22]
set_location_assignment PIN_B7 -to tmds[22]
set_location_assignment PIN_A7 -to "tmds[22](n)"

set_instance_assignment -name IO_STANDARD LVDS -to tmds[26]
set_location_assignment PIN_B11 -to tmds[26]
set_location_assignment PIN_A11 -to "tmds[26](n)"

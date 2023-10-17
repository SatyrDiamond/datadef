# DataDef: Data Definition Decode (not finished)

a binary structure parser, outputs as python dictionary

## Main
| Action Type | Info | Last Part |
| --- | --- | --- |
| ```def_start``` | Structure Name |  |
| ```def_end``` | Structure End |  |
| ```part``` | Output Data | Value Name |
| ```part_loop``` | Output Data (loop until end) | Value Name |
| ```part_iso_n``` | Output Data (Isolated), valuetype at start for data length | Value Name |
| ```setvar``` | same as ```part``` but set as varible | Var Name |
| ```pointer``` | add to pointer list | Pointer Name |
| ```pointset``` | add to pointerset list, must be list of numbers | PointerSet Name |
| ```act_pointer``` | Structure Name, Pointer Name | |
| ```act_pointset``` | Structure Name, PointerSet Name | |
| ```header``` | Length, same as ```part``` but must be number | Hex Data |

## Part
| datatype | Name | Comma Arguments | DataType Arguments |
| --- | --- | --- | --- |
| ```skip``` | Skip | Length | |
| ```byte``` | Byte | | |
| ```s_byte``` | Signed Byte | | |
| ```short``` | Short (Little) | | |
| ```short_b``` | Short (Big) | | |
| ```s_short``` | Signed Short (Little) | | |
| ```s_short_b``` | Signed Short (Big) | | |
| ```int``` | Int (Little) | | |
| ```int_b``` | Int (Big) | | |
| ```s_int``` | Signed Int (Little) | | |
| ```s_int_b``` | Signed Int (Big) | | |
| ```float``` | Float (Little) | | |
| ```float_b``` | Float (Big) | | |
| ```double``` | Double (Little) | | |
| ```double_b``` | Double (Big) | | |
| ```varint``` | VarInt | | |
| ```varint_i``` | VarInt (4 bytes)| | |
| ```raw``` | Raw | Length | |
| ```raw_l``` | Raw | | Length |
| ```raw_e``` | Raw (until end) | | |
| ```string``` | String | Length | |
| ```string_l``` | String | | Length |
| ```stringf``` | String (with fixes) | Length | |
| ```stringf_l``` | String (with fixes) | | Length |
| ```string_t``` | String (until null) | | |
| ```dstring``` | String (utf16) | Length | |
| ```dstring_l``` | String (utf16) | | Length |
| ```structure``` | do structure | Struct Name| |
| ```list``` | List | Length | Type |
| ```list_l``` | List | | Length, Type |
| ```pair``` | Pair | | Type1, Type2 |
| ```mlist``` | List with multiple types | Length | Type1, Type2, ... |
| ```keyval_n``` | Key-Value | Length | StringType, ValueType |
| ```keyval_l``` | Key-Value | | Length, StringType, ValueType |
| ```getvar``` | Get Var | Var Name | |
| ```end``` | End | | |

## example
```

area_struct | main
header | raw.4 | 494d504d
part | string.26 | songame
part | byte | hilight_minor
part | byte | hilight_major
setvar | short | num_order
setvar | short | num_inst
setvar | short | num_samp
setvar | short | num_pat
setvar | short | cwtv
setvar | short | cmwt
part | short | flags
part | short | special
part | byte | globalvol
part | byte | mv
part | byte | speed
part | byte | tempo
part | byte | sep
part | byte | pwd
part | short | message_length
pointer | int | message_offset
part | int | reserved
part | list.64 / byte | chn_pan
part | list.64 / byte | chn_vol
part | list_l / getvar.num_order / byte | orders
pointset | list_l / getvar.num_inst / int | pointer_inst
pointset | list_l / getvar.num_samp / int | pointer_samp
pointset | list_l / getvar.num_pat / int | pointer_pat
act_pointset | it_instrument.pointer_inst | data_inst
act_pointset | it_sample.pointer_samp | data_samp
act_pointset | it_pattern.pointer_pat | data_samp
area_end

```

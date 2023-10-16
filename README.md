# DataDef: Data Definition Decode (not finished)

a binary structure parser, outputs as python dictionary

## Main
| Action Type | Info | Last Part |
| --- | --- | --- |
| ```def_start``` | Structure Name |  |
| ```def_end``` | Structure End |  |
| ```part``` | Output Data | Value Name |
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
| ```varint``` | VarInt | |  |
| ```raw``` | Raw | Length | |
| ```raw_l``` | Raw | | Length |
| ```string_n``` | String (with Length) | Length | |
| ```string_l``` | String (with Length) | | Length |
| ```string_t``` | String (until null) | | |
| ```subdefine``` | do define action | | |
| ```list_n``` | List | Length | Type |
| ```list_l``` | List | | Length, Type |
| ```pair``` | Pair | | Type1, Type2 |
| ```mlist``` | Multi-List | | Type1, Type2, ... |
| ```keyval_n``` | Key-Value | Length | StringType, ValueType |
| ```keyval_l``` | Key-Value | | Length, StringType, ValueType |
| ```getvar``` | Get Var | Var Name | |

## example
```

area_struct | main
header           |raw.4                              |494d504d
part             |string_n.26                        |song_name
part             |byte                               |hilight_minor
part             |byte                               |hilight_major
setvar           |short                              |num_order
setvar           |short                              |num_inst
setvar           |short                              |num_samp
setvar           |short                              |num_pat
setvar           |short                              |cwtv
setvar           |short                              |cmwt
part             |short                              |flags
part             |short                              |special
part             |byte                               |globalvol
part             |byte                               |mv
part             |byte                               |speed
part             |byte                               |tempo
part             |byte                               |sep
part             |byte                               |pwd
part             |short                              |message_length
pointer          |int                                |message_offset
part             |int                                |reserved
part             |list_n.64/byte                     |chn_pan
part             |list_n.64/byte                     |chn_vol
part             |list_l/getvar.num_order/byte       |orders
pointset         |list_l/getvar.num_inst/int         |pointer_inst
pointset         |list_l/getvar.num_samp/int         |pointer_samp
pointset         |list_l/getvar.num_pat/int          |pointer_pat
act_pointset     |it_instrument.pointer_inst         |data_inst
act_pointset     |it_sample.pointer_samp             |data_samp
act_pointset     |it_pattern.pointer_pat             |data_samp

area_end

```

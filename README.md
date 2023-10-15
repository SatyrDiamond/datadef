# DataDef: Data Definition Decode (not finished)

## Main
| Action Type | Info | Last Part |
| --- | --- | --- |
| ```part``` | Output Data | Value Name |
| ```setvar``` | same as ```part``` but set as varible | Var Name |
| ```pointer``` | add to pointer list | Pointer Name |
| ```pointset``` | add to pointerset list, must be list of numbers | PointerSet Name |
| ```act_pointset``` | Define Name, PointerSet Name | PointerSet Name |
| ```header``` | Length | Hex Data |

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
def_start| it_sample
header           |raw,4               |494d5053
part             |raw,12              |dos_filename
part             |skip,1              |
part             |byte                |globalvol
part             |byte                |flags
part             |byte                |defualtvolume
part             |raw,26              |name
part             |skip,2              |
part             |int                 |length
part             |int                 |loop_start
part             |int                 |loop_end
def_end
```

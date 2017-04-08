/**
 * Autogenerated by Thrift Compiler (0.9.0)
 *
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 *  @generated
 */
package ff {

import org.apache.thrift.Set;
import flash.utils.ByteArray;
import flash.utils.Dictionary;

import org.apache.thrift.*;
import org.apache.thrift.meta_data.*;
import org.apache.thrift.protocol.*;


  public class SharedStruct implements TBase   {
    private static const STRUCT_DESC:TStruct = new TStruct("SharedStruct");
    private static const KEY_FIELD_DESC:TField = new TField("key", TType.I32, 1);
    private static const VALUE_FIELD_DESC:TField = new TField("value", TType.STRING, 2);

    private var _key:int;
    public static const KEY:int = 1;
    private var _value:String;
    public static const VALUE:int = 2;

    private var __isset_key:Boolean = false;

    public static const metaDataMap:Dictionary = new Dictionary();
    {
      metaDataMap[KEY] = new FieldMetaData("key", TFieldRequirementType.DEFAULT, 
          new FieldValueMetaData(TType.I32));
      metaDataMap[VALUE] = new FieldMetaData("value", TFieldRequirementType.DEFAULT, 
          new FieldValueMetaData(TType.STRING));
    }
    {
      FieldMetaData.addStructMetaDataMap(SharedStruct, metaDataMap);
    }

    public function SharedStruct() {
    }

    public function get key():int {
      return this._key;
    }

    public function set key(key:int):void {
      this._key = key;
      this.__isset_key = true;
    }

    public function unsetKey():void {
      this.__isset_key = false;
    }

    // Returns true if field key is set (has been assigned a value) and false otherwise
    public function isSetKey():Boolean {
      return this.__isset_key;
    }

    public function get value():String {
      return this._value;
    }

    public function set value(value:String):void {
      this._value = value;
    }

    public function unsetValue():void {
      this.value = null;
    }

    // Returns true if field value is set (has been assigned a value) and false otherwise
    public function isSetValue():Boolean {
      return this.value != null;
    }

    public function setFieldValue(fieldID:int, value:*):void {
      switch (fieldID) {
      case KEY:
        if (value == null) {
          unsetKey();
        } else {
          this.key = value;
        }
        break;

      case VALUE:
        if (value == null) {
          unsetValue();
        } else {
          this.value = value;
        }
        break;

      default:
        throw new ArgumentError("Field " + fieldID + " doesn't exist!");
      }
    }

    public function getFieldValue(fieldID:int):* {
      switch (fieldID) {
      case KEY:
        return this.key;
      case VALUE:
        return this.value;
      default:
        throw new ArgumentError("Field " + fieldID + " doesn't exist!");
      }
    }

    // Returns true if field corresponding to fieldID is set (has been assigned a value) and false otherwise
    public function isSet(fieldID:int):Boolean {
      switch (fieldID) {
      case KEY:
        return isSetKey();
      case VALUE:
        return isSetValue();
      default:
        throw new ArgumentError("Field " + fieldID + " doesn't exist!");
      }
    }

    public function read(iprot:TProtocol):void {
      var field:TField;
      iprot.readStructBegin();
      while (true)
      {
        field = iprot.readFieldBegin();
        if (field.type == TType.STOP) { 
          break;
        }
        switch (field.id)
        {
          case KEY:
            if (field.type == TType.I32) {
              this.key = iprot.readI32();
              this.__isset_key = true;
            } else { 
              TProtocolUtil.skip(iprot, field.type);
            }
            break;
          case VALUE:
            if (field.type == TType.STRING) {
              this.value = iprot.readString();
            } else { 
              TProtocolUtil.skip(iprot, field.type);
            }
            break;
          default:
            TProtocolUtil.skip(iprot, field.type);
            break;
        }
        iprot.readFieldEnd();
      }
      iprot.readStructEnd();


      // check for required fields of primitive type, which can't be checked in the validate method
      validate();
    }

    public function write(oprot:TProtocol):void {
      validate();

      oprot.writeStructBegin(STRUCT_DESC);
      oprot.writeFieldBegin(KEY_FIELD_DESC);
      oprot.writeI32(this.key);
      oprot.writeFieldEnd();
      if (this.value != null) {
        oprot.writeFieldBegin(VALUE_FIELD_DESC);
        oprot.writeString(this.value);
        oprot.writeFieldEnd();
      }
      oprot.writeFieldStop();
      oprot.writeStructEnd();
    }

    public function toString():String {
      var ret:String = new String("SharedStruct(");
      var first:Boolean = true;

      ret += "key:";
      ret += this.key;
      first = false;
      if (!first) ret +=  ", ";
      ret += "value:";
      if (this.value == null) {
        ret += "null";
      } else {
        ret += this.value;
      }
      first = false;
      ret += ")";
      return ret;
    }

    public function validate():void {
      // check for required fields
      // check that fields of type enum have valid values
    }

  }

}

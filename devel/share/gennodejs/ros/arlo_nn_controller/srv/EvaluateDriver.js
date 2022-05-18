// Auto-generated. Do not edit!

// (in-package arlo_nn_controller.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class EvaluateDriverRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.weightsfile = null;
      this.maxtime = null;
    }
    else {
      if (initObj.hasOwnProperty('weightsfile')) {
        this.weightsfile = initObj.weightsfile
      }
      else {
        this.weightsfile = '';
      }
      if (initObj.hasOwnProperty('maxtime')) {
        this.maxtime = initObj.maxtime
      }
      else {
        this.maxtime = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type EvaluateDriverRequest
    // Serialize message field [weightsfile]
    bufferOffset = _serializer.string(obj.weightsfile, buffer, bufferOffset);
    // Serialize message field [maxtime]
    bufferOffset = _serializer.int64(obj.maxtime, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type EvaluateDriverRequest
    let len;
    let data = new EvaluateDriverRequest(null);
    // Deserialize message field [weightsfile]
    data.weightsfile = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [maxtime]
    data.maxtime = _deserializer.int64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.weightsfile);
    return length + 12;
  }

  static datatype() {
    // Returns string type for a service object
    return 'arlo_nn_controller/EvaluateDriverRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '6e974e786534658e37e986a811914f2e';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string weightsfile
    int64 maxtime
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new EvaluateDriverRequest(null);
    if (msg.weightsfile !== undefined) {
      resolved.weightsfile = msg.weightsfile;
    }
    else {
      resolved.weightsfile = ''
    }

    if (msg.maxtime !== undefined) {
      resolved.maxtime = msg.maxtime;
    }
    else {
      resolved.maxtime = 0
    }

    return resolved;
    }
};

class EvaluateDriverResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.time = null;
      this.dist2go = null;
      this.damage = null;
      this.energy = null;
    }
    else {
      if (initObj.hasOwnProperty('time')) {
        this.time = initObj.time
      }
      else {
        this.time = 0.0;
      }
      if (initObj.hasOwnProperty('dist2go')) {
        this.dist2go = initObj.dist2go
      }
      else {
        this.dist2go = 0.0;
      }
      if (initObj.hasOwnProperty('damage')) {
        this.damage = initObj.damage
      }
      else {
        this.damage = 0.0;
      }
      if (initObj.hasOwnProperty('energy')) {
        this.energy = initObj.energy
      }
      else {
        this.energy = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type EvaluateDriverResponse
    // Serialize message field [time]
    bufferOffset = _serializer.float64(obj.time, buffer, bufferOffset);
    // Serialize message field [dist2go]
    bufferOffset = _serializer.float64(obj.dist2go, buffer, bufferOffset);
    // Serialize message field [damage]
    bufferOffset = _serializer.float64(obj.damage, buffer, bufferOffset);
    // Serialize message field [energy]
    bufferOffset = _serializer.float64(obj.energy, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type EvaluateDriverResponse
    let len;
    let data = new EvaluateDriverResponse(null);
    // Deserialize message field [time]
    data.time = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [dist2go]
    data.dist2go = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [damage]
    data.damage = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [energy]
    data.energy = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 32;
  }

  static datatype() {
    // Returns string type for a service object
    return 'arlo_nn_controller/EvaluateDriverResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '2d14dac515607a7113301ceb653b82dc';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64 time
    float64 dist2go
    float64 damage
    float64 energy
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new EvaluateDriverResponse(null);
    if (msg.time !== undefined) {
      resolved.time = msg.time;
    }
    else {
      resolved.time = 0.0
    }

    if (msg.dist2go !== undefined) {
      resolved.dist2go = msg.dist2go;
    }
    else {
      resolved.dist2go = 0.0
    }

    if (msg.damage !== undefined) {
      resolved.damage = msg.damage;
    }
    else {
      resolved.damage = 0.0
    }

    if (msg.energy !== undefined) {
      resolved.energy = msg.energy;
    }
    else {
      resolved.energy = 0.0
    }

    return resolved;
    }
};

module.exports = {
  Request: EvaluateDriverRequest,
  Response: EvaluateDriverResponse,
  md5sum() { return 'a099938bc78c367ac254aecaded19c78'; },
  datatype() { return 'arlo_nn_controller/EvaluateDriver'; }
};

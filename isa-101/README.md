# ISA 101 Standard Library for PLCnext

ISA 101 is a grey themed HMI standard that is becoming more popular to reduce the noise for operators. PLCnext Engineer 2024 LTS has been used to develop this library to be used.

There are a number of things to define to understand how to operate it. 

__Note: This is still in development and has limitations. These will be defined but don't take it as an exclusive list. As always, get in contact if any clarification needed.__

If you have any additions that would be useful to others, please provide a PR, or contact me so it can be included.

The HMI objects, datatypes and function blocks are designed to work together.

## Datatypes
These datatypes have been defined to manage a 'variable' which contains in a structure the information required to perform control, status, alarming and debugging.

### VALALMdt

<details>
<summary>This structure is the highest level for a variable.</summary>
```
VALALMdt      : STRUCT
    v           : VALdt;        // Value structure
    a           : ALMdt;        // Alarm structure
    h           : HMIdt;        // HMI structure
    s           : INT;          // State of the variable.
    d           : WORD;         // Diagnostics
END_STRUCT
```
</details>

#### VALdt

<details>
<summary>This handles the value including additional information used in the HMI and can be passed easily to another SCADA / data collection platform.</summary>
```
VALdt       : STRUCT
    v           : REAL;         // EU value
    e           : STRING;       // engineering unit
    y           : STRING;       // type of measuing
    n           : STRING;       // Name of device
    c           : NOMCONDdt;    // Nominal operating range. Used for scaling.
END_STRUCT
```
</details>

#### ALMdt

<details>
<summary>This handles the alarm bits used in the HMI. These can be used with additional variables and logic to integrate with the Alarm Server.</summary>
```
ALMdt       : STRUCT
    SP          : rLLLHHHdt;
    alm         : xLLLHHHdt;
    sup         : xLLLHHHdt;    // supressed bits.
    i           : INT;          // alarm state: 0 = nothing, 1 = low, 2 = medium, 3 = high, 4 = urgent
    d           : WORD;         // diagnostics
    iA          : iLHSTSdt;     // provides a structure to set the severity of the alarm for ALMdt.
END_STRUCT
```
</details>

#### HMIdt

<details>
<summary>Specifically for the HMI to display relevant information.</summary>
```
HMIdt       : STRUCT
    nom         : NOMCONDdt;
    sp          : rLLLHHHdt;
    val         : REAL;
END_STRUCT
```
</details>

#### Lower Level References

<details>
<summary>Additional lower level structures referenced</summary>

__Enable bit and alarm levels.__
```
rLLLHHHdt    : STRUCT
    LL          : enREALdt := (v := 10);
    L           : enREALdt := (v := 20);
    H           : enREALdt := (v := 80);
    HH          : enREALdt := (v := 90);   
END_STRUCT
```
__Enable bit and level alarm.__
```
xLLLHHHdt    : STRUCT
    LL          : enBOOLdt;
    L           : enBOOLdt;
    H           : enBOOLdt;
    HH          : enBOOLdt;
END_STRUCT
```
```
enREALdt      : STRUCT
    enabled     : BOOL;
    v           : REAL;
END_STRUCT

enBOOLdt      : STRUCT
    enabled     : BOOL := TRUE;
    v           : BOOL;
END_STRUCT
```
__Status for the variable based on alarm.__ This is used to vary severity on the HMI of the alarm.
```
iLHSTSdt     : STRUCT
    HH          : INT := 3;
    H           : INT := 2;
    L           : INT := 2; 
    LL          : INT := 3;
END_STRUCT
```
</details>

## Function Blocks
These design behind these function blocks are to provide all the information for status and control including display on the HMI. They are also made in a way that is 'scalable'. For example, compressors utilise both fMotor and fVA to achieve the functionality of a compressor. This allows for different components and requirements to easily integrate into and utilise this library.
### fVA

<details>
<summary>This function block is designed for VALALMdt. Note the 'VA' short for VALALM. These should be instantiated for each variable in a program. There are child functions that it is dependant on which can be used if required. Note the namespaces matching the datatype.</summary>

#### Variables
##### Input
- __en__ - enable the variable to initialise. By disabling, the variable will be put into a reset condition (BOOL)
- __uVA__ - the variable defined (VALALMdt)
#### States
The variable goes through different states for information and debugging of the variable if required with associated diagnostic codes.
```
A VALALM has a lifecycle throughout a program andcan fall into different states:
    0   - Disabled
    10  - Initialising
    20  - Running
    30  - Alarms supressed (*To Complete*)
```

#### Initialisation
Initialisation is completed in the following steps of the structure:
- .v - including the engineering unit, and name of the variable/device
- .a - the alarm conditions are set
- .h - the HMI conditions and scaling is set

#### Running
Once initialisation is complete, it is put into the running state. This checks the alarms and updates the variable of the HMI.
Note: for the alarm there is no deadband or hold-on timing for the alarms.

#### Diagnostic codes
All diagnostic codes in hex, aligning with the libraries developed by Phoenix Contact.
- 0000 - Disabled
- 8100 - Initialising
- 8000 - Running
</details>

### fValve

<details>
<summary>This function block (FB) currently provides basic operation of the valve according to its datatype. This includes its command source and control.</summary>
    
#### Variables
##### Inout
- __uVA__ - the variable defined (VALALMdt)

__Known Limitations__
- Currently there is no external status from a physical valve available. The state of the valve is all handled within the FB. In addition, the local command source is to be provided instantly as no request needs to be provided.
- No enable/disable input
- No diagnostics

</details>

### fMotor
<details>
<summary>This Function Block provides control for a motor.</summary>

#### Variables
##### Input
- __en__ - enable the variable to initialise. By disabling, the variable will be put into a reset condition (BOOL)
- __n__ - name of the motor (STRING)
##### Inout
__uMotor__ - the variable defined (VALALMdt)

#### Diagnostic codes
All diagnostic codes in hex, aligning with the libraries developed by Phoenix Contact.
- 0000 - Disabled
- 8100 - Initialising
- 8000 - Running
</details>

## HMI Objects
![image](https://github.com/user-attachments/assets/01844ce9-92d1-4646-97fd-888b52a24994)

[Click here](hmi/symbols/README.md) for more information.

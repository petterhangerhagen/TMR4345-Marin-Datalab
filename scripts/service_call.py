#!/usr/bin/python3.8
import subprocess
import rospy

def change_parameters()
    state=rospy.get_param("/radar/driver/default_radar_parameters/state")
    radar_range=rospy.get_param("/radar/driver/default_radar_parameters/range")
    autoGain=rospy.get_param("/radar/driver/default_radar_parameters/autoGain")
    gain=rospy.get_param("/radar/driver/default_radar_parameters/gain")
    seaClutterType=rospy.get_param("/radar/driver/default_radar_parameters/seaClutterType")
    seaClutter=rospy.get_param("/radar/driver/default_radar_parameters/seaClutter")
    autoSideLobe=rospy.get_param("/radar/driver/default_radar_parameters/autoSideLobe")
    sideLobe=rospy.get_param("/radar/driver/default_radar_parameters/sideLobe")
    STCType=rospy.get_param("/radar/driver/default_radar_parameters/STCType")
    fastScan=rospy.get_param("/radar/driver/default_radar_parameters/fastScan")
    rainClutter=rospy.get_param("/radar/driver/default_radar_parameters/rainClutter")
    FTC=rospy.get_param("/radar/driver/default_radar_parameters/FTC")
    intReject=rospy.get_param("/radar/driver/default_radar_parameters/intReject")
    localIntReject=rospy.get_param("/radar/driver/default_radar_parameters/localIntReject")
    noiseReject=rospy.get_param("/radar/driver/default_radar_parameters/noiseReject")
    beamSharpening=rospy.get_param("/radar/driver/default_radar_parameters/beamSharpening")
    targetStretch=rospy.get_param("/radar/driver/default_radar_parameters/targetStretch")
    targetBoost=rospy.get_param("/radar/driver/default_radar_parameters/targetBoost")
    rpm=rospy.get_param("/radar/driver/default_radar_parameters/rpm")
    minSNR=rospy.get_param("/radar/driver/default_radar_parameters/minSNR")
    videoAperture=rospy.get_param("/radar/driver/default_radar_parameters/videoAperture")
    rangeTrim=rospy.get_param("/radar/driver/default_radar_parameters/rangeTrim")
    rangeRate=rospy.get_param("/radar/driver/default_radar_parameters/rangeRate")
    seaTrim=rospy.get_param("/radar/driver/default_radar_parameters/seaTrim")
    seaRate1=rospy.get_param("/radar/driver/default_radar_parameters/seaRate1")
    seaRate2=rospy.get_param("/radar/driver/default_radar_parameters/seaRate2")
    rainTrim=rospy.get_param("/radar/driver/default_radar_parameters/rainTrim")
    rainRate=rospy.get_param("/radar/driver/default_radar_parameters/rainRate")
    #dopplerSupport=rospy.get_param("/radar/driver/default_radar_parameters/dopplerSupport")
    dopplerThreshold=rospy.get_param("/radar/driver/default_radar_parameters/dopplerThreshold")
    dopplerMode=rospy.get_param("/radar/driver/default_radar_parameters/dopplerMode")


    radar_parameters = {
        "state": state,
        "range": radar_range,
        "autoGain": autoGain,
        "gain": gain,
        "seaClutterType": seaClutterType,
        "seaClutter": seaClutter,
        "autoSideLobe": autoSideLobe,
        "sideLobe": sideLobe,
        "STCType": STCType,
        "fastScan": fastScan,
        "rainClutter": rainClutter,
        "FTC": FTC,
        "intReject": intReject,
        "localIntReject": localIntReject,
        "noiseReject": noiseReject,
        "beamSharpening": beamSharpening,
        "targetStretch": targetStretch,
        "targetBoost": targetBoost,
        "rpm": rpm,
        "minSNR": minSNR,
        "videoAperture": videoAperture,
        "rangeTrim": rangeTrim,
        "rangeRate": rangeRate,
        "seaTrim": seaTrim,
        "seaRate1": seaRate1,
        "seaRate2": seaRate2,
        "rainTrim": rainTrim,
        "rainRate": rainRate,
        #"dopplerSupport": False,
        "dopplerThreshold": dopplerThreshold,
        "dopplerMode": dopplerMode
    }


    # Convert the dictionary to a string
    dict_str = "{" + ", ".join(f'{k}: {v}' for k, v in radar_parameters.items()) + "}"
    subprocess.call(["rosservice","call","/radar/driver/set_parameters",dict_str])

if __name__=="__main__":
  change_parameters()

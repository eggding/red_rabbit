# -*- coding: utf-8 -*-
# @Author  : jh.feng

import ffext
import rpc.rpc_def as rpc_def
import rpc.scene_def as scene_def
import proto.gm_config_pb2 as gm_config_pb2

def SerialList2String(listData):
    return listData.encode("utf-8")

@ffext.session_call(rpc_def.Gac2GasQueryGameConf, gm_config_pb2.syn_all_gm_config_req)
def Gac2GasQueryGameConf(nPlayerGID, reqObj):

    def _cb(err, dictData):
        rsp = gm_config_pb2.syn_all_gm_config_rsp()
        rsp.ret = 0
        if dictData["g_szCurConfigName"] is None:
            rsp.cur_use_conf = ""
        else:
            rsp.cur_use_conf = dictData["g_szCurConfigName"].encode("utf-8")
        dictData.pop("g_szCurConfigName")
        for szName, dictTmp in dictData.iteritems():
            confObj = rsp.config_arr.add()
            confObj.config_name = szName.encode("utf-8")
            confObj.pos_1_card = SerialList2String(dictTmp["pos_1_card"])
            confObj.pos_2_card = SerialList2String(dictTmp["pos_2_card"])
            confObj.pos_3_card = SerialList2String(dictTmp["pos_3_card"])
            confObj.pos_4_card = SerialList2String(dictTmp["pos_4_card"])
            confObj.card_order = SerialList2String(dictTmp["card_order"])
        ffext.send_msg_session(nPlayerGID, rpc_def.Gas2GacSynAllConfig, rsp.SerializeToString())

    ffext.call_service(scene_def.GCC_SCENE, rpc_def.Gas2GccQueryGmConfig, {}, _cb)

@ffext.session_call(rpc_def.Gac2GasOptGameConf, gm_config_pb2.opt_config_req)
def Gac2GasOptGameConf(nPlayerGID, reqObj):

    # required gm_config_opt  opt_type = 1;
    # optional config_data    conf_data = 2;

    dictData = {
        "opt_type": reqObj.opt_type,
        "config_name": reqObj.conf_data.config_name,
        "pos_1_card": reqObj.conf_data.pos_1_card,
        "pos_2_card": reqObj.conf_data.pos_2_card,
        "pos_3_card": reqObj.conf_data.pos_3_card,
        "pos_4_card": reqObj.conf_data.pos_4_card,
        "card_order": reqObj.conf_data.card_order,
    }

    def _cb(err, data):
        rsp = gm_config_pb2.opt_config_rsp()
        rsp.opt_type = data["opt_type"]
        if data["conf_name"] is None:
            rsp.cur_use_conf = ""
        else:
            rsp.cur_use_conf = data["conf_name"].encode("utf-8")

            data = data["dict_data"]
            rsp.ret_data.config_name = data["config_name"].encode("utf-8")
            rsp.ret_data.pos_1_card = data["pos_1_card"].encode("utf-8")
            rsp.ret_data.pos_2_card = data["pos_2_card"].encode("utf-8")
            rsp.ret_data.pos_3_card = data["pos_3_card"].encode("utf-8")
            rsp.ret_data.pos_4_card = data["pos_4_card"].encode("utf-8")
            rsp.ret_data.card_order = data["card_order"].encode("utf-8")

        ffext.send_msg_session(nPlayerGID, rpc_def.Gas2GacRetModifyConfig, rsp.SerializeToString())

    ffext.call_service(scene_def.GCC_SCENE, rpc_def.Gas2GccModifyGmConfig, dictData, _cb)

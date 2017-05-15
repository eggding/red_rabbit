import proto.opt_pb2 as opt_pb2
rsp = opt_pb2.syn_card_info()

listMember = [1]
for pos in listMember:
    cardInfo = rsp.list_card_info.add()
    cardInfo.pos = pos
    cardInfo.card_num = 13
    cardInfo.list_card_hist.append(10)
    cardInfo.list_card_hist.append(20)
    print(len(cardInfo.list_card_hist))
    # cardInfo.list_card_hist.pop()
    # cardInfo.list_card_hist.add()
    # cardInfo.list_card_show.add()
# print(rsp.list_card_info[0])
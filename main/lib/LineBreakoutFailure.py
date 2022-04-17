import numpy as np
from pprint import pprint
from .CrossSectionSize import cross_size
from .FindLineEq import line_equation
from .LineSide import DiagonalSide


class LineBreakoutFailure():

    def __init__(self, _data) -> None:
        self._data = _data

    def run(self):
        lines = self._data.loc[self._data['zz'].notnull()]
        lines.reset_index(inplace=True, drop=False)
        edge = -1
        pb = []
        no_pb = []
        print(lines.shape[0]-1)
        for idx in range(0, lines.shape[0]-1):
            # As linhas são os topos consecutivo
            # Para cada zigzag procurar a primeira linha que cruza
            # com o limite de duas linhas para tras
            # -Se cruza verificar:
            # --Salvar ou o start do zz ou o primeiro fechamento alem da reta
            # -Se cruza linha de tendência verificar se a próxima perna cruza de volta
            # --Se a perna de rompimento não passar mais de 30%
            # --Salvar o primeiro fechamento de volta pra dentro da reta

            # _data.iloc[idx+1],
            a_li, b_li = line_equation({"y": lines.iloc[idx]['zz'], "x": lines.iloc[idx]['index']},
                                       {"y": lines.iloc[idx+1]['zz'], "x": lines.iloc[idx+1]['index']})
            if a_li > 0:
                for idx_li in range(1, 4, 2):
                    a_eq, b_eq = line_equation({"y": lines.iloc[idx-idx_li-2]['highs'], "x": lines.iloc[idx-idx_li-2]['index']},
                                               {"y": lines.iloc[idx-idx_li]['highs'],
                                                "x": lines.iloc[idx-idx_li]['index']})
                    if a_eq >= 0:
                        break
                    if lines.iloc[idx-idx_li-2]['index'] <= edge:
                        break

                    parts = cross_size({"y": lines.iloc[idx-idx_li-2]['highs'], "x": lines.iloc[idx-idx_li-2]['index']},
                                       {"y": lines.iloc[idx-idx_li]['highs'],
                                           "x": lines.iloc[idx-idx_li]['index']},
                                       {"y": lines.iloc[idx]['zz'],
                                           "x": lines.iloc[idx]['index']},
                                       {"y": lines.iloc[idx+1]['zz'], "x": lines.iloc[idx+1]['index']})
                    next_parts = cross_size({"y": lines.iloc[idx-idx_li-2]['highs'], "x": lines.iloc[idx-idx_li-2]['index']},
                                            {"y": lines.iloc[idx-idx_li]['highs'],
                                             "x": lines.iloc[idx-idx_li]['index']},
                                            {"y": lines.iloc[idx+1]['zz'],
                                             "x": lines.iloc[idx+1]['index']},
                                            {"y": lines.iloc[idx+2]['zz'], "x": lines.iloc[idx+2]['index']})
                    # print(idx_li)
                    if parts and next_parts:
                        pb.append({'eq': (lines.iloc[idx-idx_li-2]['index'], lines.iloc[idx-idx_li]['index']),
                                   'bo_leg': (lines.iloc[idx]['index'], lines.iloc[idx+1]['index']),
                                   'bo_parts': parts,
                                   'pb_leg': (lines.iloc[idx+1]['index'], lines.iloc[idx+2]['index']),
                                   'pb': next_parts
                                   })
                        edge = lines.iloc[idx-idx_li-2]['index']
                    if parts and not next_parts:
                        no_pb.append({'eq': (lines.iloc[idx-idx_li-2]['index'], lines.iloc[idx-idx_li]['index']),
                                      'bo_leg': (lines.iloc[idx]['index'], lines.iloc[idx+1]['index']),
                                      'bo_parts': parts
                                      })
        self.pb = pb
        self.no_pb = no_pb
        # pprint(pb)
        # print("no_pb: ", len(no_pb))

    # def TPnSl(self):
    #     # Se cruzou para cima pegar primeir fechamento ou start
    #     for idx in self._data.index:
    #         self

    def operation_no_pb(self):
        starts = self._data.loc[self._data['start'].notnull()]
        starts.reset_index(inplace=True, drop=False)
        entries_no_pb = []
        for item in self.no_pb:
            start_idx = starts.loc[(starts['index'] > item['bo_leg'][0]) & (
                starts['index'] <= item['bo_leg'][1])]
            if start_idx.shape[0] > 0 and start_idx.iloc[0]['index'] >= item['bo_parts'][0]:
                sl_size = abs(
                    self._data.iloc[item['bo_leg'][0]]['zz']-start_idx.iloc[0]['start'])
                entries_no_pb.append(
                    {'entry': start_idx.iloc[0]['index'], 'sl_size': sl_size})
            else:
                for idx in range(item['bo_parts'][0], item['bo_leg'][1]):
                    dia = DiagonalSide({"y": self._data.iloc[item['eq'][0]]['zz'], "x": item['eq'][0]}, {
                        "y": self._data.iloc[item['eq'][1]]['zz'], "x": item['eq'][1]},
                        {"y": self._data.iloc[idx]['close'], "x": idx})
                    if dia > 0:
                        sl_size = abs(self._data.iloc[item['bo_leg'][0]]['zz'] -
                                      self._data.iloc[idx]['close'])
                        entries_no_pb.append(
                            {"entry": idx, "sl_size": sl_size})
                        break
        # print(entries_no_pb)
        self.entries_no_pb = entries_no_pb

    def operation_with_pb(self):
        starts = self._data.loc[self._data['start'].notnull()]
        starts.reset_index(inplace=True, drop=False)
        entries_with_pb = []
        for item in self.pb:
            pprint(item)
            start_idx = starts.loc[(starts['index'] > item['bo_leg'][0]) & (
                starts['index'] <= item['bo_leg'][1])]

            if start_idx.shape[0] > 0 and start_idx.iloc[0]['index'] >= item['bo_parts'][0]:
                pprint(item)
                pb_back = starts.loc[(starts['index'] > item['pb'][0]) & (
                    starts['index'] <= item['pb'][1])]

                # print("Start:", start_idx.iloc[0]['index'])
                sl_size = 0
                if self.start_bigger_than_pb(pb_back, item['pb'][0]):
                    sl_size = self._data.iloc[start_idx.iloc[0]['index']
                                              ]['close']-self._data.iloc[pb_back.iloc[0]['index']]['close']
                else:
                    for idx in range(item['pb'][0], item['pb_leg'][1]):
                        diag = DiagonalSide({"y": self._data.iloc[item['eq'][0]]['zz'], "x": item['eq'][0]}, {
                            "y": self._data.iloc[item['eq'][1]]['zz'], "x": item['eq'][1]},
                            {"y": self._data.iloc[idx]['close'], "x": idx})
                        if diag < 0:
                            sl_size = self._data.iloc[start_idx.iloc[0]['index']
                                                      ]['close']-self._data.iloc[idx]['close']
                entries_with_pb.append(
                    {'entry': start_idx.iloc[0]['index'], 'sl_size': sl_size})

            else:
                pprint(item)
                for idx in range(item['bo_parts'][0], item['bo_leg'][1]):
                    diag = DiagonalSide({"y": self._data.iloc[item['eq'][0]]['zz'], "x": item['eq'][0]}, {
                        "y": self._data.iloc[item['eq'][1]]['zz'], "x": item['eq'][1]},
                        {"y": self._data.iloc[idx]['close'], "x": idx})
                    if diag > 0:
                        pb_back = starts.loc[(starts['index'] > item['pb_leg'][0]) & (
                            starts['index'] <= item['pb_leg'][1])]

                        # print("idx: ", idx)
                        sl_size = 0
                        if self.start_bigger_than_pb(pb_back, item['pb'][0]):
                            sl_size = self._data.iloc[start_idx.iloc[0]['index']
                                                      ]['close']-self._data.iloc[pb_back.iloc[0]['index']]['close']
                        else:
                            for idx_pb in range(item['pb'][0], item['pb_leg'][1]):
                                diag = DiagonalSide({"y": self._data.iloc[item['eq'][0]]['zz'], "x": item['eq'][0]}, {
                                    "y": self._data.iloc[item['eq'][1]]['zz'], "x": item['eq'][1]},
                                    {"y": self._data.iloc[idx_pb]['close'], "x": idx_pb})
                                if diag < 0:
                                    sl_size = self._data.iloc[idx
                                                              ]['close']-self._data.iloc[idx_pb]['close']
                                    break
                        entries_with_pb.append(
                            {"entry": idx, "sl_size": sl_size})
                        break
        # pprint(entries_with_pb)
        self.entries_with_pb = entries_with_pb

    def start_bigger_than_pb(self, start_df, item):
        if start_df.shape[0] > 0 and start_df.iloc[0]['index'] >= item:
            return True
        return False

    def prepare_backtrader(self):
        # self.operation_no_pb()
        self.operation_with_pb()
        # bt_entries_no_pb = np.full(self._data.shape[0], np.nan)
        # for item in self.entries_no_pb:
        #     bt_entries_no_pb[item['entry']] = item['sl_size']
        # bt_entries_with_pb = np.full(self._data.shape[0], np.nan)
        # for item in self.entries_with_pb:
        #     bt_entries_with_pb[item['entry']] = item['sl_size']
        # return bt_entries_no_pb, bt_entries_with_pb

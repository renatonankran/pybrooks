import numpy as np
from pprint import pprint
import plotly.graph_objects as go
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
        pb2 = []
        no_pb = []
        print("LBF Shape data: ", lines.shape[0]-1)
        for idx in range(0, lines.shape[0]-2):
            # As linhas são os topos consecutivo
            # Para cada zigzag procurar a primeira linha que cruza
            # com o limite de duas linhas para tras
            # -Se cruza verificar:
            # --Salvar ou o start do zz ou o primeiro fechamento alem da reta
            # -Se cruza linha de tendência verificar se a próxima perna cruza de volta
            # --Se a perna de rompimento não passar mais de 30%
            # --Salvar o primeiro fechamento de volta pra dentro da reta

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

                    if parts and next_parts:
                        pb.append({'eq': (lines.iloc[idx-idx_li-2]['index'], lines.iloc[idx-idx_li]['index']),
                                   'bo_leg': (lines.iloc[idx]['index'], lines.iloc[idx+1]['index']),
                                   'bo_parts': parts,
                                   'pb_leg': (lines.iloc[idx+1]['index'], lines.iloc[idx+2]['index']),
                                   'pb_parts': next_parts
                                   })
                        edge = lines.iloc[idx-idx_li-2]['index']
                    if parts and not next_parts:
                        no_pb.append({'eq': (lines.iloc[idx-idx_li-2]['index'], lines.iloc[idx-idx_li]['index']),
                                      'bo_leg': (lines.iloc[idx]['index'], lines.iloc[idx+1]['index']),
                                      'bo_parts': parts
                                      })
                        edge = lines.iloc[idx-idx_li-2]['index']
        self.pb = pb
        self.no_pb = no_pb
        print("no_pb: ", len(no_pb))
        print("with_pb: ", len(pb))

    def operation_no_pb(self):
        starts = self._data.loc[self._data['start'].notnull()]
        starts.reset_index(inplace=True, drop=False)
        entries_no_pb = np.full(self._data.shape[0], np.nan)
        for item in self.no_pb:
            start_idx = starts.loc[(starts['index'] > item['bo_leg'][0]) & (
                starts['index'] <= item['bo_leg'][1])]
            if start_idx.shape[0] > 0 and start_idx.iloc[0]['index'] >= item['bo_parts'][0]:
                sl_size = abs(
                    self._data.iloc[item['bo_leg'][0]]['zz']-start_idx.iloc[0]['start'])
                entries_no_pb[start_idx.iloc[0]['index']] = sl_size
            else:
                for idx in range(item['bo_parts'][0], item['bo_leg'][1]):
                    dia = DiagonalSide({"y": self._data.iloc[item['eq'][0]]['zz'], "x": item['eq'][0]}, {
                        "y": self._data.iloc[item['eq'][1]]['zz'], "x": item['eq'][1]},
                        {"y": self._data.iloc[idx]['close'], "x": idx})
                    if dia > 0:
                        sl_size = abs(self._data.iloc[item['bo_leg'][0]]['zz'] -
                                      self._data.iloc[idx]['close'])
                        entries_no_pb[idx] = sl_size
                        break
        # print(entries_no_pb)
        return entries_no_pb

    def operation_with_pb(self):
        starts = self._data.loc[self._data['start'].notnull()]
        starts.reset_index(inplace=True, drop=False)
        entries_with_pb = []
        for item in self.pb:

            start_idx = starts.loc[(starts['index'] > item['bo_leg'][0]) & (
                starts['index'] <= item['bo_leg'][1])]

            if start_idx.shape[0] > 0 and start_idx.iloc[0]['index'] >= item['bo_parts'][0]:

                entries_with_pb.append(
                    {'entry': start_idx.iloc[0]['index'], 'legs': item})

            else:
                for idx in range(item['bo_parts'][0], item['bo_leg'][1]):
                    diag = DiagonalSide({"y": self._data.iloc[item['eq'][0]]['zz'], "x": item['eq'][0]}, {
                        "y": self._data.iloc[item['eq'][1]]['zz'], "x": item['eq'][1]},
                        {"y": self._data.iloc[idx]['close'], "x": idx})
                    if diag > 0:
                        entries_with_pb.append({'entry': idx, 'legs': item})
                        break
        self.entries_with_pb = entries_with_pb
        return self.find_sl_size()

    def start_bigger_than_pb(self, start_df, item):
        if start_df.shape[0] > 0 and start_df.iloc[0]['index'] >= item:
            return True
        return False

    def find_sl_size(self):
        starts = self._data.loc[self._data['start'].notnull()]
        starts.reset_index(inplace=True, drop=False)
        entries = np.full(self._data.shape[0], np.nan)
        entries_price = np.full(self._data.shape[0], np.nan)
        for item in self.entries_with_pb:
            pb_start = starts.loc[(starts['index'] > item['legs']['pb_leg'][0]) & (
                starts['index'] <= item['legs']['pb_leg'][1])]
            if self.start_bigger_than_pb(pb_start, item['legs']['pb_parts'][0]):
                sl_size = self._data.iloc[item['entry']
                                          ]['close']-self._data.iloc[pb_start.iloc[0]['index']]['close']
                entries[item['entry']] = abs(sl_size)
                entries_price[item['entry']
                              ] = self._data.iloc[pb_start.iloc[0]['index']]['close']
            else:
                for idx in range(item['legs']['pb_parts'][0], item['legs']['pb_leg'][1]):
                    diag = DiagonalSide({"y": self._data.iloc[item['legs']['eq'][0]]['zz'], "x": item['legs']['eq'][0]}, {
                        "y": self._data.iloc[item['legs']['eq'][1]]['zz'], "x": item['legs']['eq'][1]},
                        {"y": self._data.iloc[idx]['close'], "x": idx})
                    if diag < 0:
                        sl_size = self._data.iloc[item['entry']
                                                  ]['close']-self._data.iloc[idx]['close']
                        entries[item['entry']] = abs(sl_size)
                        entries_price[item['entry']
                                      ] = self._data.iloc[idx]['close']
        return entries, entries_price

    def prepare_backtrader(self):
        no_pb = self.operation_no_pb()
        with_pb = self.operation_with_pb()

        return no_pb, with_pb[0], with_pb[1]

    def plot_entries(self, b3=False, with_pb=False):
        self.run()
        if with_pb:
            self.plot_with_pb(b3)
        else:
            self.without_pb(b3)

    def without_pb(self, b3=False):
        fig = go.Figure(data=[go.Candlestick(x=self._data['time'], open=self._data['open'],
                                             high=self._data['high'],
                                             low=self._data['low'],
                                             close=self._data['close'])])

        fig.add_trace(go.Scatter(
            x=self._data.loc[(self._data['zz'].notnull())]['time'],
            y=self._data.loc[(self._data['zz'].notnull())]['zz']
        ))

        fig.add_trace(go.Scatter(
            x=self._data.loc[(self._data['start'].notnull())]['time'],
            y=self._data.loc[(self._data['start'].notnull())]['start'],
            mode="markers",
            marker=dict(color="black")))

        for item in self.no_pb:
            a, b = line_equation({'x': item['eq'][0], 'y': self._data.iloc[item['eq'][0]]['zz']},
                                 {'x': item['eq'][1], 'y': self._data.iloc[item['eq'][1]]['zz']})
            line = [a*x+b for x in [item['eq']
                                    [0], item['bo_parts'][0]]]
            fig.add_trace(go.Scatter(
                x=[self._data.iloc[item['eq'][0]]['time'],
                    self._data.iloc[item['bo_parts'][0]]['time']],
                y=line,
            ))

        if b3:
            fig.update_xaxes(
                rangebreaks=[
                    dict(bounds=["sat", "mon"]),  # hide weekends
                    # hide hours outside of 9am-6pm
                    dict(bounds=[19, 9], pattern="hour"),
                ]
            )
        else:
            fig.update_xaxes(
                rangebreaks=[
                    dict(bounds=["sat", "mon"]),  # hide weekends
                ]
            )
        fig.update_layout(xaxis_rangeslider_visible=False)

        fig.show()

    def plot_with_pb(self, b3=False):

        fig = go.Figure(data=[go.Candlestick(x=self._data['time'], open=self._data['open'],
                                             high=self._data['high'],
                                             low=self._data['low'],
                                             close=self._data['close'])])

        fig.add_trace(go.Scatter(
            x=self._data.loc[(self._data['zz'].notnull())]['time'],
            y=self._data.loc[(self._data['zz'].notnull())]['zz']
        ))

        fig.add_trace(go.Scatter(
            x=self._data.loc[(self._data['start'].notnull())]['time'],
            y=self._data.loc[(self._data['start'].notnull())]['start'],
            mode="markers",
            marker=dict(color="black")))

        for item in self.pb:
            a, b = line_equation({'x': item['eq'][0], 'y': self._data.iloc[item['eq'][0]]['zz']},
                                 {'x': item['eq'][1], 'y': self._data.iloc[item['eq'][1]]['zz']})
            line = [a*x+b for x in [item['eq']
                                    [0], item['pb_parts'][0]]]
            fig.add_trace(go.Scatter(
                x=[self._data.iloc[item['eq'][0]]['time'],
                    self._data.iloc[item['pb_parts'][0]]['time']],
                y=line,
            ))

        if b3:
            fig.update_xaxes(
                rangebreaks=[
                    dict(bounds=["sat", "mon"]),  # hide weekends
                    # hide hours outside of 9am-6pm
                    dict(bounds=[19, 9], pattern="hour"),
                ]
            )
        else:
            fig.update_xaxes(
                rangebreaks=[
                    dict(bounds=["sat", "mon"]),  # hide weekends
                ]
            )
        fig.update_layout(xaxis_rangeslider_visible=False)

        fig.show()

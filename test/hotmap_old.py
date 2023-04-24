buttons = []
    sliders = []
    traces = []
    frames = []
    for index, kw in enumerate(df.columns[5:]):
        steps = []
        first = True
        for i, (time, df_time) in enumerate(df.groupby(by='time')):
            trace_density = go.Densitymapbox(lon=df_time.lon, lat=df_time.lat, z=df_time[kw],
                                             customdata=np.stack((df_time.geoName, df_time.geoCode), axis=-1),
                                             meta=[kw, time],
                                             hovertemplate='%{customdata[0]} %{customdata[1]}<br>'
                                                           'time:%{meta[1]}<br>'
                                                           'lat: %{lat:.2f},lon:%{lon:.2f}<br>'
                                                           '%{meta[0]}:%{z}', visible=False,
                                             colorbar=dict(title={"text": kw}), zmin=0,
                                             zmid=df[kw].quantile(0.4), zmax=df[kw].quantile(0.9))

            frames.append(go.Frame(data=trace_density, name=kw + " " + time, group=kw))
            if first:
                first = not first
                traces.append(trace_density)
            steps.append(dict(
                args=[[kw + " " + time],
                      {'frame': {'duration': 0, 'redraw': True}, 'fromcurrent': True, 'mode': 'immediate',
                       'transition': {'duration': 0, 'easing': 'linear'}}],
                label=time,
                method="animate"
            ))
        sliders.append(dict(
            steps=steps,
            x=0.05,
            xanchor="left",
            y=0.1,
            yanchor="bottom",
            visible=False
        ))
        # 添加按钮
        # 按钮方法带的参数，data_update 设置 visible
        data_update = dict(visible=[False] * len(df.columns[5:]))
        data_update['visible'][index] = True
        # 更新滑块
        layout_update = dict(sliders=sliders)
        layout_update['sliders'][index]['visible'] = True
        buttons.append(dict(
            label=kw,
            method="update",
            args=[data_update, layout_update]
        ))


        # 按钮
                dict(
                          type="dropdown",
                          direction="down",
                          buttons=buttons,
                          showactive=True,
                          x=0.5,
                          xanchor="left",
                          y=1.1,
                          yanchor="top"
                      ),
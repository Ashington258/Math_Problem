"""Reusable Plotly panels and offline controls. All geometry comes from SVD."""
import json
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import get_plotlyjs
from utils.linear_algebra import fundamental_subspaces, collapse
from utils.examples import COLORS, R3_TO_R2, R2_TO_R3, SQUARE_TRAP


def scatter(points, dimension, **kwargs):
    points = np.asarray(points)
    coords = dict(x=points[:,0].tolist(), y=points[:,1].tolist())
    if dimension == 3:
        return go.Scatter3d(**coords,z=points[:,2].tolist(),**kwargs)
    return go.Scatter(**coords,**kwargs)


def space_traces(basis, key, name, extent=2.2, offset=None):
    d,k = basis.shape
    color = COLORS[key]
    offset = np.zeros(d) if offset is None else np.asarray(offset)
    common = dict(name=name,legendgroup=key,meta=dict(group=key),showlegend=False)
    if k == 0:
        return [scatter(offset[None,:],d,mode='markers',marker=dict(color=color,size=8),**common)]
    if k == 1:
        v = basis[:,0]
        ends = np.array([offset-extent*v,offset+extent*v])
        traces = [scatter(ends,d,mode='lines',line=dict(color=color,width=7),**common)]
        if d == 3:
            tip=offset+1.5*v
            traces.append(go.Cone(x=[tip[0]],y=[tip[1]],z=[tip[2]],u=[v[0]],v=[v[1]],w=[v[2]],
                                 sizemode='absolute',sizeref=.23,showscale=False,
                                 colorscale=[[0,color],[1,color]],**common))
        return traces
    if k == 2:
        a,b = basis.T
        p=np.array([offset+extent*(u*a+v*b) for u,v in [(-1,-1),(1,-1),(1,1),(-1,1)]])
        if d == 3:
            patch=go.Mesh3d(x=p[:,0],y=p[:,1],z=p[:,2],i=[0,0],j=[1,2],k=[2,3],
                            color=color,opacity=.20,flatshading=True,**common)
        else:
            patch=scatter(np.vstack([p,p[0]]),d,mode='lines',fill='toself',
                          fillcolor=hex_rgba(color,.12),line=dict(color=color,width=2),**common)
        traces=[patch,scatter(np.vstack([p,p[0]]),d,mode='lines',line=dict(color=color,width=3),**common)]
        for v in basis.T:
            traces.append(scatter(np.array([offset,offset+1.5*v]),d,mode='lines',line=dict(color=color,width=4),**common))
        return traces
    raise ValueError('Only dimensions up to 3 are drawn geometrically')


def hex_rgba(color,alpha):
    values=[int(color[i:i+2],16) for i in (1,3,5)]
    return f'rgba({values[0]},{values[1]},{values[2]},{alpha})'


def point_grid(d):
    return np.array(np.meshgrid(*([np.linspace(-2,2,5)]*d))).reshape(d,-1).T


def example_figure(A, kind):
    s=fundamental_subspaces(A)
    m,n=A.shape
    fig=make_subplots(rows=1,cols=2,specs=[[dict(type='scene' if n==3 else 'xy'),dict(type='scene' if m==3 else 'xy')]],
                      subplot_titles=[f'输入空间 / Domain · R^{n}',f'输出空间 / Codomain · R^{m}'],horizontal_spacing=.10)
    def add(trace,col):
        fig.add_trace(trace,row=1,col=col)
    for key,basis,label,col in [('kernel',s.kernel,'Kernel / N(A)',1),('row',s.row,'Row(A)',1),
                                ('column',s.column,'Col(A)',2),('left_null',s.left_null,'N(Aᵀ)',2)]:
        for trace in space_traces(basis,key,label,extent=4 if key=='column' and m==2 else 2.2):
            add(trace,col)
    if n==3:
        x0=np.array([1.,0.,0.])
        sample=x0+np.array([[0,0],[1.3,0],[-1.2,.9],[.4,-1.3]])@s.kernel.T
        # Fiber uses kernel color but its own independent toggle.
        for trace in space_traces(s.kernel,'kernel','原像平面 x₀+N(A)',1.7,offset=x0):
            trace.meta=dict(group='fiber')
            trace.visible=False
            add(trace,1)
    else:
        sample=np.array([[1.,0.],[0.,1.],[1.,1.],[-1.,.5]])
    output=sample@A.T
    names=[f'x{i}' for i in range(len(sample))]
    for pts,d,col,key in [(sample,n,1,'vectors'),(output,m,2,'outputs')]:
        add(scatter(pts,d,mode='markers',marker=dict(size=7 if col==1 else 10,color=COLORS['vector'] if col==1 else COLORS['column'],
                    line=dict(color='#E2E8F0',width=1.5)),
                    name='输入向量' if col==1 else '真实映射点 Ax',meta=dict(group=key),showlegend=False,
                    customdata=[f'{names[i]}={np.round(sample[i],3).tolist()} → Ax={np.round(output[i],3).tolist()}' for i in range(len(sample))],
                    hovertemplate='%{customdata}<extra></extra>'),col)
        if col==1:
            label_points,label_text=pts,names
        else:
            unique, inverse=np.unique(np.round(pts,10),axis=0,return_inverse=True)
            label_points=unique
            label_text=[' = '.join('Ax'+str(j) for j in np.flatnonzero(inverse==i)) for i in range(len(unique))]
        add(scatter(label_points,d,mode='text',text=label_text,
                    textposition='top center',textfont=dict(color='#E2E8F0',size=12),
                    meta=dict(group='labels'),name='映射标签',showlegend=False,hoverinfo='skip'),col)
        for p in pts:
            add(scatter(np.array([np.zeros(d),p]),d,mode='lines',line=dict(color=COLORS['vector'] if col==1 else COLORS['column'],width=2),
                        meta=dict(group=key),showlegend=False,hoverinfo='skip'),col)
    grid=point_grid(n)
    dynamic_index=len(fig.data)
    lift=kind=='lift'
    initial=np.column_stack([grid,np.zeros(len(grid))]) if lift else grid
    add(scatter(initial,m if lift else n,mode='markers',marker=dict(size=3,color='#94A3B8',opacity=.65),
                name='抬升演示 Hₜx' if lift else '输入端收缩 Cₜx',meta=dict(group='cloud'),showlegend=False,
                hovertemplate='(%{x:.2f}, %{y:.2f})<extra>演示点</extra>'),2 if lift else 1)
    frames=[]
    for i,t in enumerate(np.linspace(0,1,41)):
        pts=(1-t)*initial+t*(grid@A.T) if lift else collapse(grid,s,t)
        frames.append(go.Frame(name=str(i),data=[scatter(pts,m if lift else n)],traces=[dynamic_index]))
    fig.frames=frames
    axes=dict(gridcolor='#27334D',zerolinecolor='#64748B',color='#94A3B8',showbackground=False)
    for i,d in enumerate([n,m],1):
        if d==3:
            axis=dict(axes,range=[-4.5,4.5] if lift else [-3,3])
            scene=dict(xaxis=dict(axis,title='x' if i==1 else 'u'),yaxis=dict(axis,title='y' if i==1 else 'v'),
                       zaxis=dict(axis,title='z' if i==1 else 'w'),aspectmode='cube',
                       camera=dict(eye=dict(x=1.65,y=1.3,z=1.0)),bgcolor=COLORS['bg'])
            fig.update_layout(**{fig.get_subplot(1,i).plotly_name:scene})
        else:
            subplot=fig.get_subplot(1,i)
            fig.update_xaxes(range=[-4.5,4.5],gridcolor='#27334D',zerolinecolor='#64748B',title_text='x' if i==1 else 'u',row=1,col=i)
            fig.update_yaxes(range=[-3,3],gridcolor='#27334D',zerolinecolor='#64748B',title_text='y' if i==1 else 'v',
                             scaleanchor=subplot.xaxis.plotly_name.replace('axis',''),scaleratio=1,row=1,col=i)
    fig.update_layout(template='plotly_dark',paper_bgcolor=COLORS['bg'],plot_bgcolor=COLORS['bg'],
                      height=590,margin=dict(l=35,r=25,t=45,b=20),font=dict(family='Microsoft YaHei, sans-serif'),
                      showlegend=False,uirevision='keep-view',dragmode='orbit' if n==3 or m==3 else 'pan')
    return fig,s


def export_page(filename,title,figures):
    """Each file includes Plotly.js and its computed figure data; no CDN needed."""
    payload={}
    for key,(A,kind,label) in figures.items():
        fig,s=example_figure(A,kind)
        payload[key]=dict(figure=json.loads(fig.to_json()),matrix=A.tolist(),rank=s.rank,
                          n=A.shape[1],m=A.shape[0],label=label,kind=kind,
                          bases={name:np.round(b,6).tolist() for name,b in [('Kernel',s.kernel),('Row',s.row),('Column',s.column),('Left null',s.left_null)]})
    options=''.join(f'<option value="{key}">{item[2]}</option>' for key,item in figures.items())
    controls=''.join(f'<label><input type="checkbox" data-group="{key}" {"" if key=="fiber" else "checked"}><span style="color:{COLORS.get(key,"#E2E8F0")}">{name}</span></label>' for key,name in
                     [('kernel','Kernel'),('row','Row Space'),('vectors','Input vectors'),('column','Column Space'),('left_null','Left Null'),
                      ('outputs','Mapping points'),('labels','Mapping labels'),('cloud','点阵'),('fiber','核平移平面')])
    script=JS.replace('__DATA__',json.dumps(payload,ensure_ascii=False))
    html=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>{CSS}</style><script>{get_plotlyjs()}</script></head><body>
<main><header><div class="eyebrow">LINEAR MAP LAB · 四大子空间</div><h1>{title}</h1><p>左边输入，右边输出。拖动三维图旋转，滚轮缩放；二维输出始终使用独立坐标系。</p></header>
<div class="toolbar"><select id="example">{options}</select><span id="dimension"></span></div>
<div class="controls">{controls}</div><div id="plot"></div>
<div class="slider"><button id="play">播放</button><button id="reset">重置</button><label>Interpolation t <input id="t" type="range" min="0" max="40" value="0"><output id="tvalue">0.00</output></label></div>
<section class="cards"><div><h2>映射与维数</h2><pre id="matrix"></pre><p id="ranks"></p></div><div><h2>观察这一过程</h2><p id="explanation"></p><p id="stage"></p></div></section>
<details><summary>查看 SVD 计算的正交基（列向量）</summary><pre id="bases"></pre></details>
<footer>输入：Rⁿ = Row(A) ⊕ N(A)　　输出：Rᵐ = Col(A) ⊕ N(Aᵀ)<br>核空间与列空间属于不同端；正交配对是 Kernel ↔ Row、Column ↔ Left Null。</footer></main><script>{script}</script></body></html>'''
    target=Path(__file__).resolve().parents[1]/'output'/'html'/filename
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(html,encoding='utf-8')
    print(target)
    return target


CSS='''*{box-sizing:border-box}body{margin:0;background:#0B1020;color:#E2E8F0;font-family:"Microsoft YaHei",sans-serif}main{max-width:1240px;margin:auto;padding:28px}h1{font-weight:500;font-size:30px;margin:10px 0}p{line-height:1.7;color:#B7C3D5}header p{margin:8px 0 24px}.eyebrow{font-size:12px;letter-spacing:2px;color:#60A5FA}.toolbar,.controls,.slider{display:flex;gap:18px;align-items:center;flex-wrap:wrap}.toolbar{justify-content:space-between}select,button{background:#17223A;border:1px solid #344563;color:#E2E8F0;padding:9px 14px;border-radius:5px}.controls{font-size:13px;margin-top:20px;gap:14px}.controls label{cursor:pointer}input[type=checkbox]{accent-color:#60A5FA;margin-right:6px}.slider{padding:16px 0;border-top:1px solid #25334D}.slider label{flex:1;display:flex;align-items:center;gap:16px}input[type=range]{flex:1;accent-color:#60A5FA;min-width:120px}.cards{display:grid;grid-template-columns:1fr 1.35fr;gap:22px;margin-top:12px}.cards>div{border:1px solid #25334D;border-radius:7px;padding:18px}h2{font-size:16px;font-weight:500;margin:0 0 12px}pre{font:14px/1.6 Consolas,monospace;white-space:pre-wrap;color:#D7E3F4}details{margin:20px 0;color:#94A3B8}footer{border-top:1px solid #25334D;padding:20px 0;color:#94A3B8;font-size:13px;line-height:1.8}#stage{color:#34D399}#dimension{color:#94A3B8;font-size:14px}@media(max-width:700px){main{padding:16px}.cards{grid-template-columns:1fr}h1{font-size:24px}#plot{min-height:500px}.controls{gap:8px}}'''

JS=r'''
const data=__DATA__, plot=document.getElementById('plot'), slider=document.getElementById('t');
let current, timer=null, pending=Promise.resolve();
const boxes=[...document.querySelectorAll('[data-group]')];
function stop(){clearInterval(timer);timer=null;document.getElementById('play').textContent='播放';}
function visibility(){return plot.data.map(tr=>boxes.find(b=>b.dataset.group===tr.meta?.group)?.checked??true);}
async function syncVisibility(){await Plotly.restyle(plot,{visible:visibility()});}
function description(){const t=Number(slider.value)/40;document.getElementById('tvalue').value=t.toFixed(2);
 document.getElementById('stage').textContent=current.kind==='lift'?
  (t===1?'t=1：演示网格已落在真正的 Col(B) 平面 z=x+y。':`t=${t.toFixed(2)}：Hₜ(x,y)=(x,y,t(x+y)) 是抬升演示；绿色点始终表示真实 Bx。`):
  (t===1?'t=1：点阵只剩行空间分量；右边的 Ax 从始至终不变。':`t=${t.toFixed(2)}：Cₜ 在输入端缩小核分量，A Cₜx = Ax。`);}
function setFrame(index){pending=pending.then(async()=>{await Plotly.animate(plot,[String(index)],{mode:'immediate',frame:{duration:0,redraw:true},transition:{duration:0}});await syncVisibility();});return pending;}
async function load(key){stop();await pending;document.getElementById('example').disabled=true;current=data[key];slider.value=0;
 // New subplot dimensions require a fresh plot; clone to keep source frames immutable.
 const figure=structuredClone(current.figure);
 await Plotly.newPlot(plot,figure.data,figure.layout,{responsive:true,scrollZoom:true,displaylogo:false});
 await Plotly.addFrames(plot,figure.frames);await syncVisibility();
 const fiberBox=boxes.find(b=>b.dataset.group==='fiber');fiberBox.disabled=current.n!==3;
 document.getElementById('dimension').textContent=`${current.m} × ${current.n} 矩阵 · rank ${current.rank}`;
 document.getElementById('matrix').textContent='A =\n'+current.matrix.map(row=>'[ '+row.join('  ')+' ]').join('\n');
 document.getElementById('ranks').textContent=`输入：${current.n} = ${current.n-current.rank}（核）+ ${current.rank}（秩）\n输出：${current.m} = ${current.rank}（列）+ ${current.m-current.rank}（左核）`;
 document.getElementById('explanation').textContent=current.kind==='lift'?
 'B(x,y)=(x,y,x+y)。N(B)={0}，输入网格完整保留为二维像；三维输出空间中只有 z=x+y 的平面可达。Hₜ 是输出空间内的视觉抬升，不是跨维度的 I 与 B 相加。':
 'A 将核方向全部忽略。Cₜ=P_Row+(1−t)P_N 是输入端的收缩，真实输出 Ax 另画在右端。勾选“核平移平面”观察 x₀+N(A)；其中每个点都具有同一个输出 Ax₀。';
 if(key==='square')document.getElementById('explanation').textContent+=' 方阵反例：坐标识别后 Col(A)⊂N(A)，所以二者甚至不能组成直和；正确补空间是 Row(A)。';
 document.getElementById('bases').textContent=JSON.stringify(current.bases,null,2);description();document.getElementById('example').disabled=false;}
boxes.forEach(b=>b.addEventListener('change',()=>{pending=pending.then(syncVisibility);}));
slider.addEventListener('input',()=>{stop();description();setFrame(Number(slider.value));});
document.getElementById('play').addEventListener('click',()=>{if(timer){stop();return;}if(Number(slider.value)===40)slider.value=0;
 document.getElementById('play').textContent='暂停';timer=setInterval(()=>{let i=Number(slider.value)+1;if(i>40){stop();return;}slider.value=i;description();setFrame(i);},120);});
document.getElementById('reset').addEventListener('click',()=>{stop();slider.value=0;description();setFrame(0);});
document.getElementById('example').addEventListener('change',async e=>{stop();await pending;await load(e.target.value);});
// Initial load; expose the promise for automated acceptance checks.
window.ready=load(Object.keys(data)[0]);
'''

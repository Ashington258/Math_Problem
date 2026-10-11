"""Reproducible diagrams for random events, conditioning and Bayes.

Run: python plot_events.py
Dependencies: numpy, matplotlib, pillow; Chinese sans-serif font required.
All probabilities come from specified exact models; no simulated observations.
Nominal width: 178 mm; PNG: 600 dpi; PDF: vector.
"""
from __future__ import annotations

import json
import platform
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import patches
import numpy as np
import sci_style as ss

OUT = Path(__file__).resolve().parent
ss.DEFAULT_FONTS = ['Microsoft YaHei', 'Noto Sans CJK SC', 'SimHei', 'DejaVu Sans']
ss.apply('double', font_size=9, tick_size=8, legend_size=7.5, mathtext=False)
if ss.check_fonts()=='DejaVu Sans':
    raise RuntimeError('Install a Chinese sans-serif font.')
BLUE, ORANGE = ss.OKABE_ITO['blue'], ss.OKABE_ITO['vermillion']
FIGURES=[]


def save(fig, axs, name):
    ss.panels(fig,axs,'ABCD',x=0,y=1.035)
    pdf=OUT/(name+'.pdf')
    ss.save(fig,pdf,dpi=600,also_png=True)
    w,h=ss.output_size_mm(pdf)
    assert abs(w-178)/178<.03,(name,w)
    FIGURES.append(dict(name=name,width_mm=w,height_mm=h,png_dpi=600))
    plt.close(fig)


def tiles(ax, values, selected, *, ymax=1.6, width=.74, columns=3):
    for i,k in enumerate(values):
        x, y=i%columns, 1-i//columns
        chosen=k in selected
        ax.add_patch(patches.FancyBboxPatch((x-width/2,y-.28),width,.56,
                     boxstyle='round,pad=0.02,rounding_size=0.06',
                     facecolor=BLUE if chosen else 'white', edgecolor=BLUE if chosen else '.55',lw=1))
        ax.text(x,y,str(k),ha='center',va='center',color='white' if chosen else '.3',fontsize=11)
    ax.set(xlim=(-.65,columns-.35),ylim=(-.55,ymax),xticks=[],yticks=[])
    for spine in ax.spines.values():
        spine.set_visible(False)


def event_operations():
    fig,axs=plt.subplots(2,2,figsize=ss.figsize('double',height_mm=115),layout='constrained')
    specs=[(r'$A\cup B$',{2,4,5,6},r'$P=4/6$'),
           (r'$A\cap B$',{4,6},r'$P=2/6$'),
           (r'$A\setminus B$',{2},r'$P=1/6$'),
           (r'$A^c$',{1,3,5},r'$P=3/6$')]
    for ax,(name,selected,probability) in zip(axs.flat,specs):
        tiles(ax,range(1,7),selected)
        ax.text(.06,.99,name+'；'+probability,transform=ax.transAxes,va='top',fontsize=10)
        ax.set_xlabel('蓝色格子表示属于该事件的结果',fontsize=8)
    save(fig,axs,'01_event_operations')


def conditioning():
    fig,axs=plt.subplots(1,2,figsize=ss.figsize('double',height_mm=76),layout='constrained')
    tiles(axs[0],range(1,7),{2,4,6})
    tiles(axs[1],[4,5,6],{4,6},columns=3)
    axs[0].text(.04,.99,r'未给信息：$P(A)=3/6$',transform=axs[0].transAxes,va='top',fontsize=9)
    axs[1].text(.04,.99,r'已知 $B$：$P(A\mid B)=2/3$',transform=axs[1].transAxes,va='top',fontsize=9)
    axs[0].set_xlabel('原样本空间：6 个等可能结果\n每个结果的概率为 1/6',fontsize=8)
    axs[1].set_xlabel('只保留 B 中的 3 个等可能结果\n每个结果的条件概率为 1/3',fontsize=8)
    save(fig,axs,'02_conditioning')


def bayes():
    fig,axs=plt.subplots(1,2,figsize=ss.figsize('double',height_mm=78),layout='constrained')
    for ax,values,label in zip(axs,[[.7,.3],[70/160,90/160]],['全部产品中的来源比例','次品中的来源比例']):
        bars=ax.bar([0,1],values,color=[BLUE,ORANGE],width=.55,edgecolor='.2',linewidth=.6)
        bars[1].set_hatch('///')
        for i,v in enumerate(values):
            ax.text(i,v+.025,f'{v:.2%}',ha='center',fontsize=9)
        ax.set(xticks=[0,1],xticklabels=['工厂甲','工厂乙'],ylim=(0,1),
               xlabel=label,ylabel='概率 / 比例（无量纲）',yticks=[0,.25,.5,.75,1])
        ax.minorticks_off()
    save(fig,axs,'03_bayes_factory')


def main():
    ss.grayscale_check([BLUE, ORANGE])  # Hatching also distinguishes the factories.
    event_operations()
    conditioning()
    bayes()
    data=dict(versions=dict(python=platform.python_version(),numpy=np.__version__,matplotlib=matplotlib.__version__),
              source='exact finite probability models; no observations',figures=FIGURES,
              factory_counts=dict(A_total=7000,A_defect=70,B_total=3000,B_defect=90,total_defect=160),
              probabilities=dict(A_prior=.7,B_prior=.3,defect=.016,A_given_defect=70/160,B_given_defect=90/160))
    (OUT/'figure_manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Complete: 3 probability diagrams.')


if __name__=='__main__':
    main()

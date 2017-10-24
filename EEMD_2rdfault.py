# -*- coding: utf-8 -*-
"""
Created on Mon Oct 09 10:51:38 2017

@author: 刘常
"""

#U_base=57.7#实际应用可取历史数据中正常电压的系列平均值/额定值，也可人工手动设定，单位：V
#G0=1#失压阈值，取1V
#G1=0.9*U_base#欠压阈值，取基准值的10%下限
#G2=0.995*U_base#负误差阈值
#G3=1.005*U_base#正误差阈值
#G4=1.1*U_base#升压阈值取基准值的10%上限
#PT2rdError_base=0.5%#二次压降相对限值，I、II类电能计量装置取0.005，其他取0.002（DL／T448－2000）
#d=0.025#一次侧电压波动限制，对于随机性不规则的电压波动，低压为3%，高压为2.5%（GB/T 12326-2008）
#deltaPhase_H=125#相位差正常范围最高限值，单位：度
#deltaPhase_L=115#相位差正常范围最低限值，单位：度

#I_base=671#实际应用可取历史数据中正常电压的系列平均值/额定值，也可人工手动设定，单位：mA
#G5=50#失流阈值，取50mA
#G6=0.9*I_base#分流阈值，取基准值的10%下限
#G7=0.95*I_base#负误差阈值
#G8=1.05*I_base#正误差阈值
#G9=1.1*I_base#升压阈值取基准值的10%上限

#P0=0#正常功率基准值，可取故障发生前一段时间的平均值
#whError_base=0.002#电能表误差阈值，此处对应0.2级电能表

#PTerror_Mbase=0.002#依JJG314-2010（测量用电压互感器）标准，0.2级精度的PT误差的比差阈值
                  #在80%、100%、115%的百分数下均为0.002，其他等级精度的PT比差阈值也为同一值
#PTerror_Pbase=10#依JJG314-2010（测量用电压互感器）标准，0.2级精度的PT误差的角差阈值
                  #在80%、100%、115%的百分数下均为10'，其他等级精度的PT角差阈值也为同一值
#CTerror_Mbase5=0.75#依JJG314-2010（测量用电压互感器）标准，5%电流百分数下，0.2级精度的CT误差的比差阈值
#CTerror_Pbase5=30#依JJG314-2010（测量用电压互感器）标准，5%电流百分数下，0.2级精度的CT误差的角差阈值
#CTerror_Mbase20=0.35#依JJG314-2010（测量用电压互感器）标准，20%电流百分数下，0.2级精度的CT误差的比差阈值
#CTerror_Pbase20=15#依JJG314-2010（测量用电压互感器）标准，20%电流百分数下，0.2级精度的CT误差的角差阈值
#CTerror_Mbase100=0.2#依JJG314-2010（测量用电压互感器）标准，100%电流百分数下，0.2级精度的CT误差的比差阈值
#CTerror_Pbase100=10#依JJG314-2010（测量用电压互感器）标准，100%电流百分数下，0.2级精度的CT误差的角差阈值

#******************************************************************************
#电压互感器二次回路故障诊断：根据电压幅值来判断极性接反、失压、欠压、误差超差、升压等故障；
#                      根据二次回路压降来判断压降是否超差；
#                     根据电压波动率来判断电压波动是否超限；
#                    根据相位差来判断相位是否异常
#******************************************************************************
def PT_2rdfault(U_base,PT2rdError_base,Uwh_A,Uwh_B,Uwh_C,Up0_A,Up0_B,Up0_C,
                Up1_A,Up1_B,Up1_C,Up2_A,Up2_B,Up2_C,
                Up3_A,Up3_B,Up3_C,deltaPT2rd_A,deltaPT2rd_B,
                deltaPT2rd_C,deltaSper_A,deltaSper_B,deltaSper_C,
                phaseUAB,phaseUBC,phaseUCA):
#==============================================================================
#     if Uwh_A<-1*G0 or Uwh_B<-1*G0 or Uwh_C<-1*G0:
#         print "PT绕组或电能表极性反接"
#     #如果电能表电压为负，则为极性反接
#==============================================================================
    G0=1#失压阈值，取1V
    G1=0.9*U_base#欠压阈值，取基准值的10%下限
    G2=0.995*U_base#负误差阈值
    G3=1.005*U_base#正误差阈值
    G4=1.1*U_base#升压阈值取基准值的10%上限
    d=0.025#一次侧电压波动限制，对于随机性不规则的电压波动，低压为3%，高压为2.5%（GB/T 12326-2008）
    deltaPhase_H=125#相位差正常范围最高限值，单位：度
    deltaPhase_L=115#相位差正常范围最低限值，单位：度
    if abs(Uwh_A)<G0 or abs(Uwh_B)<G0 or abs(Uwh_C)<G0:
        print "PT二次回路失压",
    #如果电能表电压接近0则为失压（不考虑接地短路情况），取绝对值在于失压后的电压信号为噪声，含正负
        if abs(Up0_A)<G0:
            print "PT的A相绕组损坏"
        elif abs(Up0_B)<G0:
            print "PT的B相绕组损坏"
        elif abs(Up0_C)<G0:
            print "PT的C相绕组损坏"
        #如果P0点（PT出口）故障    
        elif abs(Up1_A)<G0:
            print "A相熔断器/空开熔断"
        elif abs(Up1_B)<G0:
            print "B相熔断器/空开熔断"
        elif abs(Up1_C)<G0:
            print "C相熔断器/空开熔断"
        #如果P1点（空开出口）故障    
        elif abs(Up2_A)<G0:
            print "PT端子箱A相损坏或继电器A相未切换"
        elif abs(Up2_B)<G0:
            print "PT端子箱B相损坏或继电器A相未切换"
        elif abs(Up2_C)<G0:
            print "PT端子箱C相损坏或继电器A相未切换"
        #如果P2点（继电器出口）故障        
        elif abs(Up3_A)<G0:
            print "A相接线盒连片未连接"
        elif abs(Up3_B)<G0:
            print "B相接线盒连片未连接"
        elif abs(Up3_C)<G0:
            print "C相接线盒连片未连接"
        #如果P3点（接线盒出口）故障        
        else:
            print "电能表故障或电缆损坏"
    elif Uwh_A<G1 or Uwh_B<G1 or Uwh_C<G1:
        print "PT二次回路欠压",
    #如果电能表电压小于欠压阈值，则为欠压
        if Up0_A<G1:
            print "PT的A相绕组部分短路，若为CVT，则可能A相分压器损坏"
        elif Up0_B<G1:
            print "PT的B相绕组部分短路，若为CVT，则可能B相分压器损坏"
        elif Up0_C<G1:
            print "PT的C相绕组部分短路，若为CVT，则可能C相分压器损坏"
        #如果P0点（PT出口）故障    
        elif Up2_A<G1:
            print "PT端子箱A相端子松动或继电器A相触点接触不良"
        elif Up2_B<G1:
            print "PT端子箱B相端子松动或继电器B相触点接触不良"
        elif Up2_C<G1:
            print "PT端子箱C相端子松动或继电器C相触点接触不良"
        #如果P2点（继电器出口）故障        
        elif Up3_A<G1:
            print "A相接线盒连片未拧紧"
        elif Up3_B<G1:
            print "B相接线盒连片未拧紧"
        elif Up3_C<G1:
            print "C相接线盒连片未拧紧"
        #如果P3点（接线盒出口）故障        
        else:
            print "电能表故障或电缆与部件节点接触不良"            
    elif Uwh_A<G2 or Uwh_B<G2 or Uwh_C<G2:
        print "PT二次回路负误差超差",
    #如果电能表电压在欠压阈值与负误差阈值之间，则为负误差超差
        if Up0_A<G2:
            print "PT的A相电压负误差超差"
        elif Up0_B<G2:
            print "PT的B相电压负误差超差"
        elif Up0_C<G2:
            print "PT的C相电压负误差超差"
        elif Uwh_A<G2:
            print "电能表A相电压负误差超差"
        elif Uwh_B<G2:
            print "电能表B相电压负误差超差"
        else:
            print "电能表C相电压负误差超差"
    elif Uwh_A<G3 and Uwh_B<G3 and Uwh_C<G3:
        print "PT二次回路电压幅值正常",
    #如果电能表电压在正负误差阈值之间，则为正常
    elif Uwh_A<G4 or Uwh_B<G4 or Uwh_C<G4:
        print "PT二次回路正误差超差",
    #如果电能表电压在正误差限值与升压阈值之间，则为正误差超差
        if Up0_A<G4:
            print "PT的A相电压正误差超差"
        elif Up0_B<G4:
            print "PT的B相电压正误差超差"
        elif Up0_C<G4:
            print "PT的C相电压正误差超差"
        elif Uwh_A<G4:
            print "电能表A相电压正误差超差"
        elif Uwh_B<G4:
            print "电能表B相电压正误差超差"
        else:
            print "电能表C相电压正误差超差"
    elif Uwh_A>G4 or Uwh_B>G4 or Uwh_C>G4:
        print "PT二次回路升压：若为CVT，则可能分压器损坏；或因雷击感应、人为误操作致电压上浮；\
        或其他相短路造成本相电压暂升",
        if Uwh_A>G4:
            print "请检查A相二次回路升压故障"
        elif Uwh_B>G4:
            print "请检查B相二次回路升压故障"
        else:
            print "请检查C相二次回路升压故障"
    #如果电能表电压超过了升压阈值，则为升压
    else:
        print "电压幅值正常"

    if deltaPT2rd_A>PT2rdError_base or deltaPT2rd_B>PT2rdError_base \
        or deltaPT2rd_C>PT2rdError_base:
        print "PT二次回路压降超差",
    #具体视硬件厂商可提供的数据安排计算流程：deltaError=np.sqrt(pow(f,2)+pow(0.0291*delta,2))
        if Up1_A<G1:
            print "A相熔断器或空开触点接触不良，如触点氧化、元件老化等"
        elif Up1_B<G1:
            print "B相熔断器或空开触点接触不良，如触点氧化、元件老化等"
        elif Up1_C<G1:
            print "C相熔断器或空开触点接触不良，如触点氧化、元件老化等"
        #如果P1点（熔断器或空开触点）故障    
        elif Up2_A<G1:
            print "PT端子箱A相端子松动或继电器A相触点接触不良"
        elif Up2_B<G1:
            print "PT端子箱B相端子松动或继电器B相触点接触不良"
        elif Up2_C<G1:
            print "PT端子箱C相端子松动或继电器C相触点接触不良"
        #如果P2点（继电器触点）故障        
        elif Up3_A<G1:
            print "A相接线盒连片未拧紧致接触电阻变大"
        elif Up3_B<G1:
            print "B相接线盒连片未拧紧致接触电阻变大"
        elif Up3_C<G1:
            print "C相接线盒连片未拧紧致接触电阻变大"
        #如果P3点（接线盒连片）故障        
        else:
            print "电缆本身阻抗过大"
    else:
        print "PT二次回路压降正常"
    
    if deltaSper_A>d or deltaSper_B or deltaSper_C:
        print "PT二次回路电压波动超限",
    #deltaSper=(max(S1,S2,S3,S4,S5)-min(S1,S2,S3,S4,S5))/U_N
    #电压波动计算公式：其中，S1-S5为5组数据的电压均方根值，U_N为标称额定值
        if deltaSper_A>d:
            print "A相二次回路因短路故障、接地不良、非线性负载接入、人为误操作等原因造成电压波动超限"
        elif deltaSper_B>d:
            print "B相二次回路因短路故障、接地不良、非线性负载接入、人为误操作等原因造成电压波动超限"
        else:
            print "C相二次回路因短路故障、接地不良、非线性负载接入、人为误操作等原因造成电压波动超限"
    else:
        print "PT二次回路电压波动正常"
        
    if abs(phaseUAB)>deltaPhase_H or abs(phaseUAB)<deltaPhase_L:
        print "A、B相间电压相位异常，可能发生多点接地故障"
    elif abs(phaseUBC)>deltaPhase_H or abs(phaseUBC)<deltaPhase_L:
        print "B、C相间电压相位异常，可能发生多点接地故障"
    elif abs(phaseUCA)>deltaPhase_H or abs(phaseUCA)<deltaPhase_L:
        print "C、A相间电压相位异常，可能发生多点接地故障"
    else:
        print "相间电压相位正常"
        
#******************************************************************************
#电流互感器二次回路故障诊断：根据电流幅值来判断极性接反、失流、分流、误差超差、升流等故障；
#                    根据相位差来判断相位是否异常
#待完善
#******************************************************************************    
def CT_2rdfault(I_base,Iwh_A,Iwh_B,Iwh_C,Uc0_A,Uc0_B,Uc0_C,Uc1_A,Uc1_B,Uc1_C,
                Uc2_A,Uc2_B,Uc2_C,Uc3_A,Uc3_B,Uc3_C,Ic0_A,Ic0_B,Ic0_C,
                Ic1_A,Ic1_B,Ic1_C,Ic2_A,Ic2_B,Ic2_C,Ic3_A,Ic3_B,Ic3_C,
                phaseIAB,phaseIBC,phaseICA):
#==============================================================================
#     if Iwh_A<-1*G5 or Iwh_B<-1*G5 or Iwh_C<-1*G5:
#         print "CT绕组或电能表极性反接"
#     #如果电能表电流为负，则为极性反接
#==============================================================================
    Gd=10#断线电压阈值，取10V
    G5=50#失流阈值，取50mA
    G6=0.9*I_base#分流阈值，取基准值的10%下限
    G7=0.95*I_base#负误差阈值
    G8=1.05*I_base#正误差阈值
    G9=1.1*I_base#升压阈值取基准值的10%上限
    deltaPhase_H=125#相位差正常范围最高限值，单位：度
    deltaPhase_L=115#相位差正常范围最低限值，单位：度
    if abs(Iwh_A)<G5 or abs(Iwh_B)<G5 or abs(Iwh_C)<G5:
        print "CT二次回路失流",
    #如果电能表电流接近0则为失流（不考虑接地短路情况），取绝对值在于失流后的电流信号为噪声，含正负
        if abs(Uc0_A)>Gd and abs(Uc1_A)<Gd:
            print "CT端子箱的A相端子损坏或CT的A相出口到端子箱的电缆损坏"
        elif abs(Uc0_B)>Gd and abs(Uc1_B)<Gd:
            print "CT端子箱的B相端子损坏或CT的B相出口到端子箱的电缆损坏"
        elif abs(Uc0_C)>Gd and abs(Uc1_C)<Gd:
            print "CT端子箱的C相端子损坏或CT的C相出口到端子箱的电缆损坏"
        #如果端子箱故障    
        elif abs(Uc1_A)>Gd and abs(Uc2_A)<Gd:
            print "继电器的A相未接触或CT端子箱到继电器的电缆损坏"
        elif abs(Uc1_B)>Gd and abs(Uc2_B)<Gd:
            print "继电器的B相未接触或CT端子箱到继电器的电缆损坏"
        elif abs(Uc1_C)>Gd and abs(Uc2_C)<Gd:
            print "继电器的C相未接触或CT端子箱到继电器的电缆损坏"
        #如果继电器故障    
        elif abs(Uc2_A)>Gd and abs(Uc3_A)<Gd:
            print "接线盒/端子排的A相连片未连接或继电器到接线盒/端子排的电缆损坏"
        elif abs(Uc2_B)>Gd and abs(Uc3_B)<Gd:
            print "接线盒/端子排的B相连片未连接或继电器到接线盒/端子排的电缆损坏"
        elif abs(Uc2_C)>Gd and abs(Uc3_C)<Gd:
            print "接线盒/端子排的C相连片未连接或继电器到接线盒/端子排的电缆损坏"
        #如果接线盒/端子排故障
        else:
            print "电能表故障或电缆损坏"
    elif Iwh_A<G6 or Iwh_B<G6 or Iwh_C<G6:
        print "CT二次回路分流",
    #如果电能表电流小于分流阈值，则为分流
        if Ic0_A>Ic1_A:
            print "CT端子箱的A相端子处分流或端子箱与继电器之间电缆损坏接地分流"
        elif Ic0_B>Ic1_B:
            print "CT端子箱的B相端子处分流或端子箱与继电器之间电缆损坏接地分流"
        elif Ic0_C>Ic1_C:
            print "CT端子箱的C相端子处分流或端子箱与继电器之间电缆损坏接地分流"
        #如果端子箱出口故障
        elif Ic1_A>Ic2_A:
            print "继电器与接线盒/端子排之间的A相电缆损坏接地分流"
        elif Ic1_B>Ic2_B:
            print "继电器与接线盒/端子排之间的B相电缆损坏接地分流"
        elif Ic1_C>Ic2_C:
            print "继电器与接线盒/端子排之间的C相电缆损坏接地分流"
        #如果继电器出口故障
        elif Ic2_A>Ic3_A:
            print "接线盒/端子排的A相端子处分流或接线盒/端子排与电能表之间电缆损坏接地分流"
        elif Ic2_B>Ic3_B:
            print "接线盒/端子排的B相端子处分流或接线盒/端子排与电能表之间电缆损坏接地分流"
        elif Ic2_C>Ic3_C:
            print "接线盒/端子排的C相端子处分流或接线盒/端子排与电能表之间电缆损坏接地分流"
        #如果接线盒/端子排出口故障
        else:
            print "电能表故障或电缆损坏"
    elif Iwh_A<G7 or Iwh_B<G7 or Iwh_C<G7:
        print "CT二次回路负误差超差",
    #如果电能表电流在分流阈值与负误差阈值之间，则为负误差超差
        if Ic0_A<G7:
            print "CT的A相电流负误差超差"
        elif Ic0_B<G7:
            print "PT的B相电流负误差超差"
        elif Ic0_C<G7:
            print "PT的C相电流负误差超差"
        elif Iwh_A<G7:
            print "电能表A相电流负误差超差"
        elif Iwh_B<G7:
            print "电能表B相电流负误差超差"
        else:
            print "电能表C相电流负误差超差"
    elif Iwh_A<G8 and Iwh_B<G8 and Iwh_C<G8:
        print "CT二次回路电流幅值正常"
    #如果电能表电流在正负误差阈值之间，则为正常
    elif Iwh_A<G9 or Iwh_B<G9 or Iwh_C<G9:
        print "CT二次回路正误差超差",
    #如果电能表电流在正误差限值与升压阈值之间，则为正误差超差
        if Ic0_A<G9:
            print "CT的A相电流正误差超差"
        elif Ic0_B<G9:
            print "PT的B相电流正误差超差"
        elif Ic0_C<G9:
            print "PT的C相电流正误差超差"
        elif Iwh_A<G9:
            print "电能表A相电流正误差超差"
        elif Iwh_B<G9:
            print "电能表B相电流正误差超差"
        else:
            print "电能表C相电流正误差超差"
    elif Iwh_A>G9 or Iwh_B>G9 or Iwh_C>G9:
        print "PT二次回路升流：可能二次回路接入容性负载；或因雷击感应、人为误操作致电流上升；\
               或发生多点接地故障",
    #如果电能表电流超过了正误差限值，则为升流
        if Iwh_A>G9:
            print "请检查A相升流故障"
        elif Iwh_B>G9:
            print "请检查B相升流故障"
        else:
            print "请检查C相升流故障"
    else:
        print "电流幅值正常"
    
    if abs(phaseIAB)>deltaPhase_H or abs(phaseIAB)<deltaPhase_L:
        print "A、B相间电流相位异常，可能发生多点接地故障"
    elif abs(phaseIBC)>deltaPhase_H or abs(phaseIBC)<deltaPhase_L:
        print "B、C相间电流相位异常，可能发生多点接地故障"
    elif abs(phaseICA)>deltaPhase_H or abs(phaseICA)<deltaPhase_L:
        print "C、A相间电流相位异常，可能发生多点接地故障"
    else:
        print "CT二次回路电流相位正常"
    
#******************************************************************************    
#窃电故障诊断，主要有改变电压的窃电、改变电流的窃电、改变相位的窃电等    
#这里指的窃电是广义窃电，即只要存在电压、电流或相位改变，均可认为发生窃电，不论故意还是无意
#******************************************************************************
def eleSteal_fault(U_base,I_base,Uwh_A,Uwh_B,Uwh_C,Iwh_A,Iwh_B,Iwh_C,Pwh,
                   phase_UIA,phase_UIB,phase_UIC):
    G0=1#失压阈值，取1V
    G1=0.9*U_base#欠压阈值，取基准值的10%下限
    G5=50#失流阈值，取50mA
    G6=0.9*I_base#分流阈值，取基准值的10%下限
    if abs(Uwh_A)<G0 or abs(Uwh_B)<G0 or abs(Uwh_C)<G0:
        print "PT二次回路失压窃电，可能情况为TV的熔断器断开或TV二次回路装设开关，随时断开电压进行窃电",
    #条件同PT二次回路失压故障，侧重人为原因
        if abs(Uwh_A)<G0:
            print "请检查A相PT二次回路"
        elif abs(Uwh_B)<G0:
            print "请检查B相PT二次回路"
        else:
            print "请检查C相PT二次回路"
    elif Uwh_A<G1 or Uwh_B<G1 or Uwh_C<G1:
        print "PT二次回路欠压窃电，可能情况为：虚接电压线，将电压线芯线揉断，或外层塑料未剥直接\
               压接，采用电容分压，减小电压线圈电压",
    #条件同PT二次回路欠压故障，侧重人为原因
        if Uwh_A<G1:
            print "请检查A相PT二次回路"
        elif Uwh_B<G1:
            print "请检查B相PT二次回路"
        else:
            print "请检查C相PT二次回路"
    else:
        print "PT二次回路未出现失压窃电或欠压窃电故障"
    
    if abs(Iwh_A)<G5 or abs(Iwh_B)<G5 or abs(Iwh_C)<G5:
        print "CT二次回路失流窃电，可能情况为CT二次侧断开",
    #条件同CT二次回路失流故障，侧重人为原因
        if Iwh_A<G5:
            print "请检查A相CT二次回路"
        elif Iwh_B<G5:
            print "请检查B相CT二次回路"
        else:
            print "请检查C相CT二次回路"
    elif Iwh_A<G6 or Iwh_B<G6 or Iwh_C<G6:
        print "CT二次回路分流窃电，可能情况为：改变TA变比，将大电流比的TA铭牌换成小电流比的CT名牌；\
               把CT的P1端与P2端短接，使大部分电流不经过TA的一次绕组，从而绕过电能计量装置窃电；\
               二次回路外接分支负载分流",
    #条件同CT二次回路失流故障，侧重人为原因
        if Iwh_A<G6:
            print "请检查A相CT二次回路"
        elif Iwh_B<G6:
            print "请检查B相CT二次回路"
        else:
            print "请检查C相CT二次回路"
    else:
        print "CT二次回路未出现失流窃电或分流窃电故障"
    
    if abs(phase_UIA)>60 or abs(phase_UIB)>60 or abs(phase_UIC)>60:
        print "互感器绕组电压、电流相序或极性接反，详见接线错误故障诊断模块",
        if abs(phase_UIA)>60:
            print "请检查A相绕组"
        elif abs(phase_UIB)>60:
            print "请检查B相绕组"
        else:
            print "请检查C相绕组"
    else:
        print "二次回路未出现电压、电流相序或极性反接窃电故障"

#******************************************************************************    
#接线错误故障诊断，主要有断线、极性反接等    
#这里的故障诊断逻辑不考虑相序接反、短路；需获取有功、电压电流幅值相位等数据
#******************************************************************************
def line_fault(P0,Pwh,Uwh_A,Uwh_B,Uwh_C,Iwh_A,Iwh_B,Iwh_C,
               phase_UIA,phase_UIB,phase_UIC):
    G0=1#失压阈值，取1V
    G5=50#失流阈值，取50mA
    if Pwh>0.9*2*P0/3 and Pwh<1.1*2*P0/3:
        if abs(Uwh_A)<G0 or abs(Iwh_A)<G5:
            print "A相电压二次回路断线或电流二次回路断线"
        elif abs(Uwh_B)<G0 or abs(Iwh_B)<G5:
            print "B相电压二次回路断线或电流二次回路断线"
        elif abs(Uwh_C)<G0 or abs(Iwh_C)<G5:
            print "C两相电压二次回路断线或电流二次回路断线"
        #一相断线故障可导致功率降为约正常值的2/3        
    elif Pwh>0.9*P0/3 and Pwh<1.1*P0/3:
        if (abs(Uwh_A)<G0 and abs(Uwh_B)<G0) or (abs(Iwh_A)<G5 and abs(Iwh_B))<G5:
            print "A、B两相电压二次回路断线或电流二次回路断线"
        elif (abs(Uwh_B)<G0 and abs(Uwh_C)<G0) or (abs(Iwh_B)<G5 and abs(Iwh_C))<G5:
            print "B、C两相电压二次回路断线或电流二次回路断线"
        elif (abs(Uwh_A)<G0 and abs(Uwh_C)<G0) or (abs(Iwh_A)<G5 and abs(Iwh_C))<G5:
            print "A、C两相电压二次回路断线或电流二次回路断线"
        #两相断线故障可导致功率降为约正常值的1/3
        if abs(phase_UIA)>90:
            print "A相二次回路电压或电流极性反接"
        elif abs(phase_UIB)>90:
            print "B相二次回路电压或电流极性反接"
        elif abs(phase_UIC)>90:
            print "C相二次回路电压或电流极性反接"
        #一相电压或电流极性反接可导致功率降为约正常值的1/3    
    elif Pwh>0.9*G0*G5 and Pwh<1.1*G0*G5:
        if (abs(Uwh_A)<G0 and abs(Uwh_B)<G0 and abs(Uwh_C)<G0)\
            or (abs(Iwh_A)<G5 and abs(Iwh_B)<G5 and abs(Iwh_C))<G5:
            print "A、B、C三相电压二次回路断线或电流二次回路断线"
        #三相断线故障可导致功率降为零值
        if abs(phase_UIA)>90 and (abs(Uwh_B)<G0 or abs(Iwh_B)<G5):
            print "A相二次回路电压或电流极性反接，B相电压或电流二次回路断线"
        elif abs(phase_UIA)>90 and (abs(Uwh_C)<G0 or abs(Iwh_C)<G5):
            print "A相二次回路电压或电流极性反接，C相电压或电流二次回路断线"
        elif abs(phase_UIB)>90 and (abs(Uwh_C)<G0 or abs(Iwh_C)<G5):
            print "B相二次回路电压或电流极性反接，C相电压或电流二次回路断线"
        elif abs(phase_UIB)>90 and (abs(Uwh_A)<G0 or abs(Iwh_A)<G5):
            print "B相二次回路电压或电流极性反接，A相电压或电流二次回路断线"
        elif abs(phase_UIC)>90 and (abs(Uwh_A)<G0 or abs(Iwh_A)<G5):
            print "C相二次回路电压或电流极性反接，A相电压或电流二次回路断线"
        elif abs(phase_UIC)>90 and (abs(Uwh_B)<G0 or abs(Iwh_B)<G5):
            print "C相二次回路电压或电流极性反接，B相电压或电流二次回路断线"        
        #一相电压或电流极性反接，另一相电压或电流二次回路断线可导致功率降为零值    
    elif Pwh<-0.9*P0 and Pwh>-1.1*P0:
        if abs(phase_UIA)>90 and abs(phase_UIB)>90:
            print "A、B相二次回路电压或电流极性反接"        
        elif abs(phase_UIB)>90 and abs(phase_UIC)>90:
            print "B、C相二次回路电压或电流极性反接"
        elif abs(phase_UIC)>90 and abs(phase_UIA)>90:
            print "C、A相二次回路电压或电流极性反接"
        #二次回路两相电压或电流极性反接可导致功率变为负正常值
        if abs(Uwh_A)<G0 and abs(Uwh_B)<G0 and abs(phase_UIC)>90:
            print "A、B两相电压二次回路断线或电流二次回路断线，C相二次回路电压或电流极性反接"
        if abs(Uwh_B)<G0 and abs(Uwh_C)<G0 and abs(phase_UIA)>90:
            print "B、C两相电压二次回路断线或电流二次回路断线，A相二次回路电压或电流极性反接"
        if abs(Uwh_C)<G0 and abs(Uwh_A)<G0 and abs(phase_UIB)>90:
            print "C、A两相电压二次回路断线或电流二次回路断线，B相二次回路电压或电流极性反接"                
        #两相电压或电流二次回路断线，另一相电压或电流极性反接可导致功率变为负正常值    
    elif Pwh<-0.9*2*P0 and Pwh>-1.1*2*P0:
        if abs(phase_UIA)>90 and abs(phase_UIB)>90\
              and (abs(Uwh_C)<G0 or abs(Iwh_C)<G5):
            print "A、B相二次回路电压或电流极性反接，C相电压或电流二次回路断线"        
        elif abs(phase_UIB)>90 and abs(phase_UIC)>90\
              and (abs(Uwh_A)<G0 or abs(Iwh_A)<G5):
            print "B、C相二次回路电压或电流极性反接，A相电压或电流二次回路断线"
        elif abs(phase_UIC)>90 and abs(phase_UIA)>90\
              and (abs(Uwh_B)<G0 or abs(Iwh_B)<G5):
            print "C、A相二次回路电压或电流极性反接，B相电压或电流二次回路断线"
        #二次回路两相电压或电流极性反接，另一相电压或电流二次回路断线可导致功率变为负两倍的正常值 
    else:
        print "二次回路接线正常"
        
#******************************************************************************    
#电能表误差超差诊断    
#包括主电能表和副电能表两项内容
#******************************************************************************
def whErrorDiag(whError_base,whError_main,whError_affi):
    if whError_main>whError_base:
        print "主电能表正误差超差"
    elif whError_main<-whError_base:
        print "主电能表负误差超差"
    elif whError_affi>whError_base:
        print "副电能表正误差超差"
    elif whError_affi<-whError_base:
        print "副电能表负误差超差"
    else:
        print "主副电能表误差正常"
        
#******************************************************************************    
#电压互感器误差超差诊断    
#包括电压互感器在下限负荷下，不同电压百分数的比值差和相角差（不计误差正负）:根据现场测试数据，下限负荷误差较额定负荷误差大
#******************************************************************************
#Lpt=[]#PTerror2_AM80,PTerror2_AP80,PTerror2_BM80,PTerror2_BP80,PTerror2_CM80,PTerror2_CP80,
      #PTerror2_AM100,PTerror2_AP100,PTerror2_BM100,PTerror2_BP100,PTerror2_CM100,PTerror2_CP100,
      #PTerror2_AM115,PTerror2_AP115,PTerror2_BM115,PTerror2_BP115,PTerror2_CM115,PTerror2_CP115
def PTerrorDiag(PTaccuracy_grade,Lpt):
    if PTaccuracy_grade==0.5:
        PTerror_Mbase=0.5
        PTerror_Pbase=20
    elif PTaccuracy_grade==0.2:
        PTerror_Mbase=0.2
        PTerror_Pbase=10
    elif PTaccuracy_grade==0.1:
        PTerror_Mbase=0.10
        PTerror_Pbase=5.0
    elif PTaccuracy_grade==0.05:
        PTerror_Mbase=0.05
        PTerror_Pbase=2.0
    elif PTaccuracy_grade==0.02:
        PTerror_Mbase=0.02
        PTerror_Pbase=0.6
    #根据PT精度等级确定比差和角差阈值
    
    if abs(Lpt[0])>PTerror_Mbase:
        print "下限负荷、80%额定电压下，PT的A相比差超差"
    elif abs(Lpt[1])>PTerror_Pbase:
        print "下限负荷、80%额定电压下，PT的A相角差超差"
    elif abs(Lpt[2])>PTerror_Mbase:
        print "下限负荷、80%额定电压下，PT的B相比差超差"
    elif abs(Lpt[3])>PTerror_Pbase:
        print "下限负荷、80%额定电压下，PT的B相角差超差"
    elif abs(Lpt[4])>PTerror_Mbase:
        print "下限负荷、80%额定电压下，PT的C相比差超差"
    elif abs(Lpt[5])>PTerror_Pbase:
        print "下限负荷、80%额定电压下，PT的C相角差超差"
        
    elif abs(Lpt[6])>PTerror_Mbase:
        print "下限负荷、100%额定电压下，PT的A相比差超差"
    elif abs(Lpt[7])>PTerror_Pbase:
        print "下限负荷、100%额定电压下，PT的A相角差超差"
    elif abs(Lpt[8])>PTerror_Mbase:
        print "下限负荷、100%额定电压下，PT的B相比差超差"
    elif abs(Lpt[9])>PTerror_Pbase:
        print "下限负荷、100%额定电压下，PT的B相角差超差"
    elif abs(Lpt[10])>PTerror_Mbase:
        print "下限负荷、100%额定电压下，PT的C相比差超差"
    elif abs(Lpt[11])>PTerror_Pbase:
        print "下限负荷、100%额定电压下，PT的C相角差超差"
        
    elif abs(Lpt[12])>PTerror_Mbase:
        print "下限负荷、115%额定电压下，PT的A相比差超差"
    elif abs(Lpt[13])>PTerror_Pbase:
        print "下限负荷、115%额定电压下，PT的A相角差超差"
    elif abs(Lpt[14])>PTerror_Mbase:
        print "下限负荷、115%额定电压下，PT的B相比差超差"
    elif abs(Lpt[15])>PTerror_Pbase:
        print "下限负荷、115%额定电压下，PT的B相角差超差"
    elif abs(Lpt[16])>PTerror_Mbase:
        print "下限负荷、115%额定电压下，PT的C相比差超差"
    elif abs(Lpt[17])>PTerror_Pbase:
        print "下限负荷、115%额定电压下，PT的C相角差超差"
    
    else:
        print "PT误差正常"
        
#******************************************************************************    
#电流互感器误差超差诊断    
#包括电流互感器在额定负荷下，不同电流百分数的比值差和相角差（任选一组变比，电流百分数选择5%、20%和100%，不计误差正负）：根据现场测试数据，额定负荷较下限负荷的误差大
#******************************************************************************
#Lct=[]#依次为CTerror1_AM5,CTerror1_AP5,CTerror1_BM5,CTerror1_BP5,CTerror1_CM5,CTerror1_CP5,
      #CTerror1_AM20,CTerror1_AP20,CTerror1_BM20,CTerror1_BP20,CTerror1_CM20,CTerror1_CP20，        
      #CTerror1_AM100,CTerror1_AP100,CTerror1_BM100,CTerror1_BP100,CTerror1_CM100,CTerror1_CP100
      
def CTerrorDiag(CTaccuracy_grade,Lct):
    if CTaccuracy_grade==0.5:
        CTerror_Mbase5=1.5
        CTerror_Pbase5=90
        CTerror_Mbase20=0.75
        CTerror_Pbase20=45
        CTerror_Mbase100=0.5
        CTerror_Pbase100=30
    elif CTaccuracy_grade==0.2:
        CTerror_Mbase5=0.75
        CTerror_Pbase5=30
        CTerror_Mbase20=0.35
        CTerror_Pbase20=15
        CTerror_Mbase100=0.2
        CTerror_Pbase100=10
    elif CTaccuracy_grade==0.1:
        CTerror_Mbase5=0.4
        CTerror_Pbase5=15
        CTerror_Mbase20=0.2
        CTerror_Pbase20=8
        CTerror_Mbase100=0.1
        CTerror_Pbase100=5
    elif CTaccuracy_grade==0.05:
        CTerror_Mbase5=0.05
        CTerror_Pbase5=2
        CTerror_Mbase20=0.05
        CTerror_Pbase20=2
        CTerror_Mbase100=0.05
        CTerror_Pbase100=2
    elif CTaccuracy_grade==0.02:
        CTerror_Mbase5=0.02
        CTerror_Pbase5=0.6
        CTerror_Mbase20=0.02
        CTerror_Pbase20=0.6
        CTerror_Mbase100=0.02
        CTerror_Pbase100=0.6
    #根据CT精度等级确定比差和角差阈值
        
    if abs(Lct[0])>CTerror_Mbase5:
        print "5%额定电流下，CT的A相比差超差"
    elif abs(Lct[1])>CTerror_Pbase5:
        print "5%额定电流下，CT的A相角差超差"
    elif abs(Lct[2])>CTerror_Mbase5:
        print "5%额定电流下，CT的B相比差超差"
    elif abs(Lct[3])>CTerror_Pbase5:
        print "5%额定电流下，CT的B相角差超差"
    elif abs(Lct[4])>CTerror_Mbase5:
        print "5%额定电流下，CT的C相比差超差"
    elif abs(Lct[5])>CTerror_Pbase5:
        print "5%额定电流下，CT的C相角差超差"
        
    elif abs(Lct[6])>CTerror_Mbase20:
        print "20%额定电流下，CT的A相比差超差"
    elif abs(Lct[7])>CTerror_Pbase20:
        print "20%额定电流下，CT的A相角差超差"
    elif abs(Lct[8])>CTerror_Mbase20:
        print "20%额定电流下，CT的B相比差超差"
    elif abs(Lct[9])>CTerror_Pbase20:
        print "20%额定电流下，CT的B相角差超差"
    elif abs(Lct[10])>CTerror_Mbase20:
        print "20%额定电流下，CT的C相比差超差"
    elif abs(Lct[11])>CTerror_Pbase20:
        print "20%额定电流下，CT的C相角差超差"
        
    elif abs(Lct[12])>CTerror_Mbase100:
        print "100%额定电流下，CT的A相比差超差"
    elif abs(Lct[13])>CTerror_Pbase100:
        print "100%额定电流下，CT的A相角差超差"
    elif abs(Lct[14])>CTerror_Mbase100:
        print "100%额定电流下，CT的B相比差超差"
    elif abs(Lct[15])>CTerror_Pbase100:
        print "100%额定电流下，CT的B相角差超差"
    elif abs(Lct[16])>CTerror_Mbase100:
        print "100%额定电流下，CT的C相比差超差"
    elif abs(Lct[17])>CTerror_Pbase100:
        print "100%额定电流下，CT的C相角差超差"
    
    else:
        print "CT误差正常"
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

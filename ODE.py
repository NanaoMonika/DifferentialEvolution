__author__ = 'Hojjat Salehinejad'
import time
import sys
import numpy as np
import random
import fgeneric
import bbobbenchmarks as bn
import os
import logging

def saver(path_to_savein, data_to_save, name_file):
    if not os.path.exists(path_to_savein):
        os.makedirs(path_to_savein)
    path_to_save = path_to_savein + '/' + name_file + '.txt'
    np.savetxt(path_to_save, data_to_save)

def mutation_scheme_maker(_ms_type, _ms_list, NP, _ms_indx):
    # map: p1  pb  p2-p3  p1-p2  p3-p4  p4-p5  p_current pb-p_current x_avg_b
    ms_dic = {'rand1': [1, 0, 1, 0, 0, 0, 0, 0],  # x1+F(x2-x3)
    'best1': [0, 1, 0, 1, 0, 0, 0, 0],  #
    'tbest1': [0, 0, 0, 1, 0, 0, 1, 1],
    'rand2':[1, 0, 1, 0, 0, 1, 0, 0],
    'best2':[0, 1, 0, 1, 1, 0, 0, 0],
    }
    len_ms_dic = len(ms_dic[_ms_list[0]])
    len_ms_list = len(_ms_list)
    mut_sh_mask = np.zeros((NP, len_ms_dic))

    if _ms_type == 'static':
        for indv in range(NP):
            mut_sh_mask[indv,:] = ms_dic[_ms_list[_ms_indx]]  # takes the first mutation scheme
    elif _ms_type == 'population':
        for indv in range(NP):
            mut_sh_mask[indv, :] = ms_dic[_ms_list[np.random.randint(len_ms_list)]]  # takes random mutation scheme
    return mut_sh_mask


def Parent_Selection(_NP, _POP, _cost):
    P1 = np.zeros((NP, D))
    P2 = np.zeros((NP, D))
    P3 = np.zeros((NP, D))
    P4 = np.zeros((NP, D))
    P5 = np.zeros((NP, D))

    if _NP > 5:
        soreted_index = sorted(range(len(_cost)),key=lambda x:_cost[x])  # index of ascending sorted values
        P_avg_best = np.mean(_POP[soreted_index[0:3]], axis=0)  # average of three top best individuals
        P_best = _POP[soreted_index[0]]  # best individual
        for indv in range(_NP):
            cand_indx = range(0, _NP)  # list of candidate parents
            del cand_indx[indv]  # remove current individual
            random.shuffle(cand_indx)  # shuffle the list of candidate parents

            P1[indv, :] = _POP[cand_indx[0]]
            P2[indv, :] = _POP[cand_indx[1]]
            P3[indv, :] = _POP[cand_indx[2]]
            P4[indv, :] = _POP[cand_indx[3]]
            P5[indv, :] = _POP[cand_indx[4]]
    else:
        raise ValueError('Population size is less than 5.')

    return P1, P2, P3, P4, P5, P_best, P_avg_best


def F_Generator(NP, D, F_flag):
    if F_flag == "Cte":
        F = 0.5*np.ones((NP, D))
    elif F_flag == "Scalar":
        F = 0 + (2-0)*(np.ones((NP, 1))*np.random.rand(1, D))
    elif F_flag == "Vector":
        F = 0 + (2-0)*(np.random.rand(NP, D))
    return F


def Mutation(_pop, _parents, fu, ms_mask, NP, D):

    p1 = _parents[0]
    p2 = _parents[1]
    p3 = _parents[2]
    p4 = _parents[3]
    p5 = _parents[4]
    pb = _parents[5]
    p_avg_best = _parents[6]

    v_in = np.zeros((NP, D))
    for p in range(NP):
        pi = _pop[p,:]
        for d in range(D):

            v_in[p][d] = ms_mask[p][0]*p1[p][d] + ms_mask[p][1]*pb[d] + ms_mask[p][2]*fu[p][d]*(p2[p][d] - p3[p][d])\
                         + ms_mask[p][3]*fu[p][d]*(p1[p][d] - p2[p][d])\
                         + ms_mask[p][4]*fu[p][d]*(p3[p][d] - p4[p][d]) \
                     + ms_mask[p][5]*fu[p][d]*(p4[p][d] - p5[p][d])\
                         + ms_mask[p][6]*pi[d]\
                         + ms_mask[p][7]*fu[p][d]*(pb[d] - pi[d])

    return v_in


def CrossOver(_pop, v, cr, D, NP):
    cross_pop = np.zeros((NP,D))
    for ind_indx in range(NP):
        I_rand = np.random.randint(D)
        for d in range(D):

            rann = random.random()

            if rann <= cr or d == I_rand:
                cross_pop[ind_indx][d] = v[ind_indx][d]
            elif rann > cr and d != I_rand:
                cross_pop[ind_indx][d] = _pop[ind_indx][d]

    return cross_pop


def mp_handler(_pop, _f):
    cost = _f.evalfun(_pop)
    return cost


def Selection(_pop, _New_U, _Cost_CU, _Cost_POP, _NP):
    _new_pop = _pop
    _Cost_New_POP = _Cost_POP

    for pc in range(_NP):
        if _Cost_CU[pc] <= _Cost_POP[pc]:
            _new_pop[pc, :] = _New_U[pc,:]
            _Cost_New_POP[pc] = _Cost_CU[pc]
    return _new_pop, _Cost_New_POP


def similarity_counter(_POP,_OPOP):
    counter = 0
    for i,j in zip(_POP,_OPOP):
        if np.all(i==j):
            counter+=1
    return counter

#python DE.py 1 10 'Cte' 'static' 30 0 100
if __name__ == '__main__':
    script_name = os.path.basename(__file__)    
    for hojji in range(1,2):
        All_Result_Avg = []
        All_Result_BSF = []
        All_Result_POP = []
        All_Result_Std = []
        All_Result_Err = []
        All_Result_NFC = []
        All_Result_Err_last = []
        BSF_Epoch = []

        FId = int(sys.argv[1])
        D = int(sys.argv[2])  # Number of Dimensions
        F_flag = sys.argv[3]  # "Vector"  # Cte, Scalar, Vector
        ms_type = sys.argv[4]  # 'population'  # population  static individual
        NP = int(sys.argv[5]) # 20  # Population Number
        ms_indx = sys.argv[6]  # index of mutation scheme
        Bound = int(sys.argv[7])
        Cr = 0.5  # CrossOver Rate
        VTR = 1e-8  # Value to Reach
        N_Epoch = 1  # Number of Epochs
        NFC = 10000*D  # Number of Function Calls
        LB = -Bound  #
        UB = Bound  # Upper bound
        f_gen = fgeneric.LoggingFunction('tmp').setfun(*bn.instantiate(FId))
        OGV = f_gen.ftarget  # Optimal Global Value to Reach
        readme_log = 'D:' + str(D) + ' NP:' + str(NP) + ' NFC:' + str(NFC) + \
                     ' MF:' + F_flag + ' MST:' + ms_type + ' MSI:' + str(ms_indx) + \
                     ' Limit:' + str(Bound) + 'N_Epoch:' + str(N_Epoch) + ' Cr:' + str(Cr) + ' VTR:' + str(VTR)

        logging.basicConfig(filename=script_name[:-3]+'.log', level=logging.INFO)
        logging.info(readme_log)

        ms_list = ['rand1', 'best1', 'tbest1', 'best2', 'rand2']

        if ms_indx == 'null':
            ms_indx = 'null'
        else:
            ms_indx = int(ms_indx)

        
        mut_scheme_mask = mutation_scheme_maker(ms_type, ms_list, NP, ms_indx)

        for epoch in range(1, N_Epoch+1):
            gc = 1
            FC_C = 0  # function call counter
            FC_C_list = []
            POP = LB*np.ones((NP, D)) + np.random.rand(NP, D)*(UB*np.ones((NP, D))-(LB*np.ones((NP, D))))
            Cost_POP = mp_handler(POP, f_gen)

            # Opposition
            OPOP = LB + UB - POP  # Added Opposition
            pop_similarity_count = similarity_counter(POP, OPOP)  # count similarity between pop and opop
            Cost_OPOP = mp_handler(OPOP, f_gen)
            Cost_APOP = np.concatenate((Cost_POP, Cost_OPOP))
            APOP = np.vstack([POP, OPOP])
            indx_top_cost = Cost_APOP.argsort()[:NP]
            POP = APOP[indx_top_cost]
            Cost_POP = Cost_APOP[indx_top_cost]

            # Collect Results
            Result_Avg = []
            Result_BSF = []
            Result_POP = []
            Result_Std = []
            Result_Err = []

            BSF = min(Cost_POP)  # Best So Far
            Result_Avg.append(np.mean(Cost_POP))
            Result_BSF.append(BSF)
            min_index = np.argmin(Cost_POP)
            Result_POP.append(POP[min_index, ])
            Result_Std.append(np.std(Cost_POP))
            Result_Err.append(abs(BSF-OGV))

            FC_C = NP*D + NP*D - pop_similarity_count*D  # function call counter
            FC_C_list.extend([FC_C])
            
            while (abs(BSF - OGV) > VTR) & (FC_C <= NFC):
                F = F_Generator(NP, D, F_flag)

                parents = Parent_Selection(NP, POP, Cost_POP)

                V = Mutation(POP, parents, F, mut_scheme_mask, NP, D)

                U = CrossOver(POP, V, Cr, D, NP)
                Cost_new_U = mp_handler(U, f_gen)

                New_POP, Cost_New_POP = Selection(POP, U, Cost_new_U, Cost_POP, NP)  # make POP

                # Opposition
                OPOP = LB + UB - New_POP  # Added Opposition
                pop_similarity_count = similarity_counter(New_POP, OPOP)  # count similarity between pop and opop
                Cost_OPOP = mp_handler(OPOP, f_gen)
                Cost_APOP = np.concatenate((Cost_New_POP, Cost_OPOP))
                APOP = np.vstack([New_POP, OPOP])
                indx_top_cost = Cost_APOP.argsort()[:NP]
                New_POP = APOP[indx_top_cost]
                Cost_New_POP = Cost_APOP[indx_top_cost]

                # Update
                POP = New_POP
                Cost_POP = Cost_New_POP

                BSF = min(Cost_POP)

                Result_Avg.append(np.mean(Cost_POP))
                Result_BSF.append(BSF)
                Index = list(Cost_POP).index(BSF)

                Result_POP.append(POP[Index, ])
                Result_Std.append(np.std(Cost_POP))
                Result_Err.append(abs(BSF-OGV))

                if gc%10 == 0:
                    print '++++++++++++++++++'
                    print abs(BSF - OGV)
                    print 'Fid is:', FId
                    print 'epoch is:', epoch
                gc = gc + 1
                FC_C = FC_C + D*NP + D*NP - pop_similarity_count*D
                FC_C_list.extend([FC_C])

            if FC_C < NFC:  # make equal length lists
                tail_Std = [np.std(Cost_POP)]*((NFC-FC_C)/(NP*D))
                Result_Std.extend(tail_Std)                

                tail_Avg = [np.mean(Cost_POP)]*((NFC-FC_C)/(NP*D))
                Result_Avg.extend(tail_Avg)    

                tail_BSF = [BSF]*((NFC-FC_C)/(NP*D))
                Result_BSF.extend(tail_BSF)    

                tail_POP = [POP[Index, ]]*((NFC-FC_C)/(NP*D))
                Result_POP.extend(tail_POP)    

                tail_Err = [abs(BSF-OGV)]*((NFC/(NP*D))-(FC_C/(NP*D)))
                Result_Err.extend(tail_Err)                
          
            All_Result_Avg.append(Result_Avg)
            All_Result_BSF.append(Result_BSF)
            All_Result_NFC.append([FC_C])
            All_Result_Std.append(Result_Std)
            All_Result_Err.append(Result_Err)

            name_saver = ['All_Result_Avg', 'All_Result_BSF', 'All_Result_Err',
                         'All_Result_Std', 'All_Result_NFC']
            name_saver_var = [All_Result_Avg, All_Result_BSF, All_Result_Err,
                              All_Result_Std, All_Result_NFC]

            for name_id in range(len(name_saver)):
                mypath = script_name[:-3] + '_Results/' + 'D' + str(D) + 'NP' + str(NP) + 'NFC' + str(NFC) + 'MF' + F_flag + '_MST' + ms_type + '_MSI' + str(ms_indx) + 'F' + str(FId)

                saver(mypath, name_saver_var[name_id], name_saver[name_id])



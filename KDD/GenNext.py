# APIs used to generate next document prediction in time series.
# Project still in progress, and this script is not a stable release.

class GenNext:
	# def __init__(self):


	@staticmethod
	def plotPerf (sorted_result, xlab, ylab, title, legloc):
	'''
	Used to evaluate performance of a single source of data
	'''
	    x_axis = []
	    PCs = []
	    MRR1s = []
	    MRR2s = []
	    for i in sorted_result:
	        x_axis.append(i[0])
	        PCs.append(i[1][0])
	        MRR1s.append(i[1][1])
	        MRR2s.append(i[1][2])

	    plt.plot(x_axis, PCs, color="green", linewidth=2.5, linestyle="-", label="PC")
	    plt.plot(x_axis, MRR1s, color="blue", linewidth=2.5, linestyle="-", label="MRR_strict")
	    plt.plot(x_axis, MRR2s, color="red", linewidth=2.5, linestyle="-", label="MRR_lib")
	    plt.legend(loc=legloc)
	    plt.xlabel(xlab)
	    plt.ylabel(ylab)
	    plt.title(title)

    @staticmethod
    def plotPerf2 (resultwant, result1, result2, xlab, ylab, title, legloc): # ety first
    '''
    Used to compare performances of two results
    '''
	    x_axis1 = []
	    PCs1 = []
	    MRR1s1 = []
	    MRR2s1 = []
	    for i in result1:
	        x_axis1.append(i[0])
	        PCs1.append(i[1][0])
	        MRR1s1.append(i[1][1])
	        MRR2s1.append(i[1][2])

	    x_axis2 = []
	    PCs2 = []
	    MRR1s2 = []
	    MRR2s2 = []
	    for i in result2:
	        x_axis2.append(i[0])
	        PCs2.append(i[1][0])
	        MRR1s2.append(i[1][1])
	        MRR2s2.append(i[1][2])
	    if resultwant == 'PC':
	        plt.plot(x_axis1, PCs1, color="red", linewidth=2.5, linestyle="-", label="PC_ety")
	        plt.plot(x_axis2, PCs2, color="blue", linewidth=2.5, linestyle="-", label="PC_wc")
	    if resultwant == 'MRR_Strict':
	        plt.plot(x_axis1, MRR1s1, color="red", linewidth=2.5, linestyle="-", label="MRR_strict_ety")
	        plt.plot(x_axis2, MRR1s2, color="blue", linewidth=2.5, linestyle="-", label="MRR_strict_wc")
	    if resultwant == 'MRR_Lib':
	        plt.plot(x_axis1, MRR2s1, color="red", linewidth=2.5, linestyle="-", label="MRR_lib_ety")
	        plt.plot(x_axis2, MRR2s2, color="blue", linewidth=2.5, linestyle="-", label="MRR_lib_wc")
	    plt.legend(loc=legloc)
	    plt.xlabel(xlab)
	    plt.ylabel(ylab)
	    plt.title(title)

    @staticmethod
    def genNextUuidsOnePhase(firstSource, topWhat, candidate):
    '''
	Generate next doc in one phase manner (i.e. only consider the poll instead of the exact one).
    '''

	    # nextUuidTopWhat = {}
	    nextUuidTopWhatLite = {}
	    # nextUuidPred = {}
	    for i in candidate:
	        # 1st stage of candidate generation, using enity comparison (Jaccard) + date time restriction
	        dateTimeSelect = uuidAndDateTime[i]
	        sorted_jac_sim = sorted(firstSource[i].items(), key=operator.itemgetter(1), reverse=True)
	        candidate_tmp = [] # jsut uuid, no rank score
	        # candidate_s1 = [] # uuid and rank score
	        cnt = 0
	        for j in sorted_jac_sim[1:]: # sorted_jac_sim is a list of tuples, (uuid, similarity_score)
	            if uuidAndDateTime[j[0]] >= dateTimeSelect:
	                # candidate_s1.append((j[0],j[1]))
	                candidate_tmp.append(j[0])          #### speed boost: choose time sufficient first, then pick them out
	                cnt += 1
	                if cnt == topWhat:
	                    break
	        # nextUuidTopWhat[i] = candidate_s1
	        nextUuidTopWhatLite[i] = candidate_tmp

	    # return (nextUuidTopWhat, nextUuidTopWhatLite, nextUuidPred)
	    return nextUuidTopWhatLite

    @staticmethod
    def evaluation(nextUuidTopWhatLite, candAndNext):
    '''
	Perform evaluations: PC, MRR1, MRR2.
    '''
	    rank = {}
	    for (i, j) in candAndNext.items():
	        if len(j) == 1: # only one correct answer
	            try:
	                rank[i] = nextUuidTopWhatLite[i].index(j[0]) + 1
	            except:
	                rank[i] = -1
	        else: # have multiple correct answers
	            tmprank = []
	            for k in j:
	                try:
	                    tmprank.append(nextUuidTopWhatLite[i].index(k) + 1)
	                except:
	                    pass
	            if len(tmprank) == 0:
	                rank[i] = -1
	            else:
	                rank[i] = min(tmprank) # pick the best rank

	    cnt = 0
	    for i in rank.values():
	        if i != -1:
	            cnt += 1

	    PC = cnt / len(candAndNext)

	    # MRR in n + 1 mode, MRR1 = MRR_strict
	    MRR1 = 0
	    for i in rank.values():
	        if i != -1:
	            MRR1 += 1 / i
	    MRR1 = MRR1 / len(rank)

	    MRR in n mode, MRR2 = MRR_lib
	    MRR2 = 0
	    numbers = 0
	    for i in rank.values():
	         if i != -1:
	             MRR2 += 1 / i
	             numbers += 1
	    
	    if numbers == 0: numbers += 1 # avoid divide by zero
	    
	    MRR2 = MRR2 / numbers

	    return [PC, MRR1, MRR2]
	    # return [PC, MRR1]

    @staticmethod
    def genNextUuidsSoftOnePhase(firstSource, threshold, candidate):
    '''
	Generate next uuid based on the threshold. 
    '''
	    nextUuidTopWhat = {}
	    nextUuidTopWhatLite = {}
	    nextUuidPred = {}

	    for i in candidate:

	        dateTimeSelect = uuidAndDateTime[i]
	        sorted_jac_sim = sorted(firstSource[i].items(), key=operator.itemgetter(1), reverse=True)
	        candidate_tmp = []  # jsut uuid, no rank score
	        candidate_s1 = []  # uuid and rank score

	        for j in sorted_jac_sim[1:]:  # sorted_jac_sim is a list of tuples, (uuid, similarity_score)
	            if uuidAndDateTime[j[0]] >= dateTimeSelect: ###
	                if (j[1] >= threshold):
	                    candidate_s1.append((j[0], j[1]))
	                    candidate_tmp.append(j[0])
	                elif (j[1] < threshold):
	                    # if threshold == 0: ##
	                    #    print (i, j[0], j[1]) ##
	                    break
	        nextUuidTopWhat[i] = candidate_s1
	        nextUuidTopWhatLite[i] = candidate_tmp

	    return (nextUuidTopWhat, nextUuidTopWhatLite, nextUuidPred)

    @staticmethod
    def genNextUuids(firstSource, secondSource, topWhat, shuffle, candidate):
    """
	Generate next uuid based on poll size.

    input:
    firstSource: pairWiseJacEntityReg or pairWiseJacReg
    secondSource: pairWiseJacEntityReg or pairWiseJacReg
    topWhat:keep how many docs in first round
    mode: no shuffle or shuffle before 2nd round, 1 shuffle, 0 no shuffle
    candidate: candidate list

    output: nextUuidTopWhat,nextUuidPred

    """
	    nextUuidTopWhat = {}
	    nextUuidTopWhatLite = {}
	    nextUuidPred = {}
	    for i in candidate:
	        # 1st stage of candidate generation, using enity comparison (Jaccard) + date time restriction
	        dateTimeSelect = uuidAndDateTime[i]
	        sorted_jac_sim = sorted(firstSource[i].items(), key=operator.itemgetter(1), reverse=True)
	        candidate_tmp = [] # jsut uuid, no rank score
	        candidate_s1 = [] # uuid and rank score
	        cnt = 0
	        for j in sorted_jac_sim: # sorted_jac_sim is a list of tuples, (uuid, similarity_score)
	            if uuidAndDateTime[j[0]] >= dateTimeSelect:
	                candidate_s1.append((j[0],j[1]))
	                candidate_tmp.append(j[0])          #### speed boost: choose time sufficient first, then pick them out
	                cnt += 1
	                if cnt == topWhat:
	                    break
	        nextUuidTopWhat[i] = candidate_s1
	        nextUuidTopWhatLite[i] = candidate_tmp

	        # 2nd stage of candidate generation
	        if (shuffle == 0):
	            # no shuffle, keep orig seq, using word cloud comparison (Jaccard) to break ties
	            # check if there is a tie
	            tmplist = []
	            topsimval = firstSource[i][candidate_tmp[0]]
	            for j in candidate_tmp:
	                if firstSource[i][j] == topsimval:
	                    tmplist.append(j)

	            if (len(tmplist) == 1):
	                nextUuidPred[i] = tmplist[0]
	            else:  # use wc jaccard
	                tmpjac = {}
	                for k in tmplist:
	                    tmpjac[k] = secondSource[i][k]
	                sorted_tmpjac = sorted(tmpjac.items(), key=operator.itemgetter(1), reverse=True)
	                nextUuidPred[i] = sorted_tmpjac[0][0]
	                # DVCounter += 1

	        elif (shuffle == 1):
	            lrgsim = -1
	            candi = ''
	            for x in candidate_tmp:
	                if secondSource[i][x] > lrgsim:
	                    lrgsim = secondSource[i][x]
	                    candi = x
	            nextUuidPred[i] = candi


	    return (nextUuidTopWhat, nextUuidTopWhatLite, nextUuidPred)

    @staticmethod
	def genNextUuidsSoft(firstSource, secondSource, threshold, shuffle, candidate):
	'''
	Generate next uuid based on threshold. 
	'''

	    nextUuidTopWhat = {}
	    nextUuidTopWhatLite = {}
	    nextUuidPred = {}

	    for i in candidate:

	        # 1st stage of candidate generation, using enity comparison (Jaccard) + date time restriction
	        dateTimeSelect = uuidAndDateTime[i]
	        sorted_jac_sim = sorted(firstSource[i].items(), key=operator.itemgetter(1), reverse=True)
	        candidate_tmp = []  # jsut uuid, no rank score
	        candidate_s1 = []  # uuid and rank score

	        for j in sorted_jac_sim:  # sorted_jac_sim is a list of tuples, (uuid, similarity_score)
	            if uuidAndDateTime[j[0]] >= dateTimeSelect: ###
	                if (j[1] >= threshold):
	                    candidate_s1.append((j[0], j[1]))
	                    candidate_tmp.append(j[0])
	                elif (j[1] < threshold):
	                    # if threshold == 0: ##
	                    #    print (i, j[0], j[1]) ##
	                    break
	        nextUuidTopWhat[i] = candidate_s1
	        nextUuidTopWhatLite[i] = candidate_tmp

	        # 2nd stage of candidate generation
	        if (shuffle == 0):
	            # no shuffle, keep orig seq, using word cloud comparison (Jaccard) to break ties
	            # check if there is a tie
	            tmplist = []
	            if len(candidate_tmp) > 0:
	                topsimval = firstSource[i][candidate_tmp[0]]
	                for j in candidate_tmp:
	                    if firstSource[i][j] == topsimval:
	                        tmplist.append(j)

	            if len(tmplist) == 1:
	                nextUuidPred[i] = tmplist[0]
	            elif len(tmplist) == 0:
	                nextUuidPred[i] = []
	            else:  # use wc jaccard
	                tmpjac = {}
	                for k in tmplist:
	                    tmpjac[k] = secondSource[i][k]
	                sorted_tmpjac = sorted(tmpjac.items(), key=operator.itemgetter(1), reverse=True)
	                nextUuidPred[i] = sorted_tmpjac[0][0]
	                # DVCounter += 1

	        elif (shuffle == 1):
	            lrgsim = -1
	            candi = ''
	            if len(candidate_tmp) == 0:
	                nextUuidPred[i] = []
	            elif len(candidate_tmp) == 1:
	                nextUuidPred[i] = candidate_tmp[0]
	            else:
	                for x in candidate_tmp:
	                    if secondSource[i][x] > lrgsim:
	                        lrgsim = secondSource[i][x]
	                        candi = x
	                nextUuidPred[i] = candi

	            # counter += 1
	            # print counter / tot

	    return (nextUuidTopWhat, nextUuidTopWhatLite, nextUuidPred)

	# this is efficient tester
	@staticmethod
	def Tester(candidate, firstSource, candAndNext, pool):
	'''
	Effcieient tester to generate test results.
	'''

	# def TesterForTime(candidate, candAndNext, pool): # use when time only

	    nextUuidTopWhatLite = genNextUuidsOnePhase(firstSource, pool, candidate)
	    # nextUuidTopWhatLite = genNextUuidsTimeOnly(pool, candidate) # use when time only
	    rank = {}
	    for (i, j) in candAndNext.items():
	        if len(j) == 1:
	            try:
	                rank[i] = nextUuidTopWhatLite[i].index(j[0]) + 1
	            except:
	                rank[i] = -1
	        else:
	            tmprank = []
	            for k in j:
	                try:
	                    tmprank.append(nextUuidTopWhatLite[i].index(k) + 1)
	                except:
	                    pass
	            if len(tmprank) == 0:
	                rank[i] = -1
	            else:
	                rank[i] = min(tmprank)

	    xAxis = range(1, 1001)
	    yAxisPC = [0 for i in range(1, 1001)]
	    yAxisMRR_s = [0 for i in range(1, 1001)]
	    length = len(candAndNext)

	    for (i, j) in rank.items():
	        if j != -1:  # only consider the results that appear in top what
	            cnt1 = j
	            while (cnt1 - 1 < len(yAxisPC)):
	                yAxisPC[cnt1 - 1] += 1
	                yAxisMRR_s[cnt1 - 1] += 1 / j
	                cnt1 += 1

	    yAxisPC = [i / length for i in yAxisPC]
	    yAxisMRR_s = [i / length for i in yAxisMRR_s]
	    outcome = dict(zip(xAxis, zip(yAxisPC, yAxisMRR_s)))

	    print "finished"

	    return outcome


	# this is an inefficient tester, for more efficient version, check Tester above
	@staticmethod
	# def Test(mode, candidate, firstSource, secondSource, candAndNext):
	def Test(candidate, firstSource, candAndNext):
	'''
	Inefficient tester to generate test results.
	Still useful when only one result is needed.
	'''
	    start = 1
	    result = {}
	    while (start <= 1000):
	        # (nextUuidTopWhat, nextUuidTopWhatLite, nextUuidPred) = genNextUuids(firstSource, secondSource, start, mode, candidate)
	        nextUuidTopWhatLite = genNextUuidsOnePhase(firstSource, start, candidate)
	        
	        [PC, MRR1, MRR2] = evaluation(nextUuidTopWhatLite, candAndNext)
	        # [PC, MRR1] = evaluation(nextUuidTopWhatLite, candAndNext)
	        result[start] = [PC, MRR1, MRR2]
	        # result[start] = [PC, MRR1]
	        print str(start) + "/1000 finished"
	        start += 10

	    return result


	# def TestSoft(mode, candidate, firstSource, secondSource, candAndNext):
	def TestSoft(candidate, firstSource, candAndNext):
	'''
	Inefficient tester to generate test results.
	Still useful when only one result is needed.
	'''

	    x_range = range(0,21)
	    x_range = [i/100 for i in x_range]
	    result = {}
	    for i in x_range: # 0.2
	        #(nextUuidTopWhat, nextUuidTopWhatLite, nextUuidPred) = genNextUuidsSoft(firstSource, secondSource, i, mode, candidate)
	        (nextUuidTopWhat, nextUuidTopWhatLite, nextUuidPred) = genNextUuidsSoftOnePhase(firstSource, i, candidate)

	        [PC, MRR1, MRR2] = evaluation(nextUuidTopWhatLite, candAndNext)
	        result[i] = [PC, MRR1, MRR2]

	        print str(i / 0.2) + " finished"

	    return result





















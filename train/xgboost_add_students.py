#!/usr/bin/python
import numpy as np
import scipy.sparse
import xgboost as xgb
### simple example
# load file from text file, also binary buffer generated by xgboostdtrain = xgb.DMatrix('../data/agaricus.txt.train')

ftr_x = open('./xgb_input_add_users.csv', 'r')
te_mat = []
for trxline in ftr_x:
    splited = trxline.split(",")
    te_mat.insert(len(te_mat), [int(splited[1]), int(splited[2]), int(splited[3]), int(splited[4]), int(splited[5]), \
                                int(splited[6]), int(splited[7]), int(splited[8]), int(splited[9]), int(splited[10])])

arr_idx = 0
ftr_y = open('./truth_train.csv', 'r')
for tryline in ftr_y:
    splited = tryline.split(",")
    te_mat[arr_idx].insert(0, int(splited[1]))
    arr_idx = arr_idx + 1

te_np_arr = np.array(te_mat)
dtrain = xgb.DMatrix(te_np_arr[:,1:11], label=te_np_arr[:,0])
#dtrain = xgb.DMatrix(te_np_arr[:,8], label=te_np_arr[:,0])
#dtrain = xgb.DMatrix(te_np_arr[:,1:10], label=te_np_arr[:,0])
# specify parameters via map, definition are same as c++ version
param = {'max_depth':2, 'eta':1, 'silent':1, 'objective':'binary:logistic' }

# specify validations set to watch performance
watchlist  = [(dtrain,'train')]
num_round = 200
bst = xgb.train(param, dtrain, num_round, watchlist)

fts = open('../test/xgb_input_add_users.csv', 'r')
enroll_ids = []
ts_mat = []
for tsline in fts:
    splited = tsline.split(",")
    enroll_ids.insert(len(enroll_ids), splited[0])
    ts_mat.insert(len(ts_mat), [int(splited[1]), int(splited[2]), int(splited[3]), int(splited[4]), int(splited[5]), \
                                int(splited[6]), int(splited[7]), int(splited[8]), int(splited[9]), int(splited[10])])

ts_np_arr = np.array(ts_mat)
#dtest = xgb.DMatrix(ts_np_arr[:,1:9], label=ts_np_arr[:,0])
dtest = xgb.DMatrix(ts_np_arr)

# this is prediction
preds = bst.predict(dtest)

print str(len(preds))
print str(len(enroll_ids))

frslt = open('../test/xgb_ccc_2_200.csv', 'w')
for idx in xrange(len(enroll_ids)):
    frslt.write(enroll_ids[idx] + "," + str(preds[idx]) + "\n")

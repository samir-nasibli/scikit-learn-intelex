#*******************************************************************************
# Copyright 2014-2018 Intel Corporation
# All Rights Reserved.
#
# This software is licensed under the Apache License, Version 2.0 (the
# "License"), the following terms apply:
#
# You may not use this file except in compliance with the License.  You may
# obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#*******************************************************************************

# daal4py Decision Forest Regression Tree Traversal example

import math
import daal4py as d4p
from numpy import loadtxt, allclose


def printTree(nodes, values):
    def printNodes(node_id, nodes, values, level):
        node = nodes[node_id]
        value = values[node_id]
        if not math.isnan(node["threshold"]):
            print(" " * level + "Level " + str(level) + ": Feature = " + str(node["feature"]) + ", Threshold = " + str(node["threshold"]))
        else:
            print(" " * level + "Level " + str(level) + ", Value = " + str(value).replace(" ", ""))
        if node["left_child"] != -1:
            printNodes(node["left_child"], nodes, values, level + 1)
        if node["right_child"] != -1:
            printNodes(node["right_child"], nodes, values, level + 1)
        return

    printNodes(0, nodes, values, 0)
    return


if __name__ == "__main__":
    # input data file
    infile = "./data/batch/df_regression_train.csv"

    # Configure a training object
    train_algo = d4p.decision_forest_regression_training(nTrees=2, minObservationsInLeafNode=8, featuresPerNode=13, varImportance="MDI",
                                                         bootstrap=True, resultsToCompute="computeOutOfBagError")

    # Read data. Let's have 13 independent, and 1 dependent variables (for each observation)
    indep_data = loadtxt(infile, delimiter=',', usecols=range(13))
    dep_data = loadtxt(infile, delimiter=',', usecols=range(13, 14)).reshape((-1, 1))  # must be a 2d array

    # Now train/compute, the result provides the model for prediction, outOfBagError, outOfBagErrorPerObservation, variableImportance
    train_result = train_algo.compute(indep_data, dep_data)

    # Retrieve Tree State for 1 Tree as encoded in sklearn.ensamble.tree_.Tree
    treeId = 0
    treeState = d4p.getTreeState(train_result.model, treeId)
    printTree(treeState.node_ar, treeState.value_ar)

'''
Runs the streamlit app
Call this file in the terminal via `streamlit run app.py`
'''
from streamlit_extras.badges import badge

import streamlit as st

from streamlit_extras.colored_header import colored_header
from streamlit_option_menu import option_menu

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split as TTS
from sklearn.model_selection import cross_val_score as CVS
from sklearn.model_selection import cross_validate as CV

from sklearn.metrics import make_scorer, r2_score
from sklearn.model_selection import LeaveOneOut
from sklearn import tree

from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor as RFR
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.linear_model import LinearRegression as LinearR
from sklearn.linear_model import LogisticRegression as LR
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.neural_network import MLPRegressor

from sklearn.svm import SVR
from sklearn.svm import SVC
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import mutual_info_regression as MIR
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix
from sklearn.metrics import r2_score
from sklearn.metrics import make_scorer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor

import xgboost as xgb
from catboost import CatBoostClassifier
from catboost import CatBoostRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
import Bgolearn.BGOsampling as BGOS


import graphviz

import shap
import matplotlib.pyplot as plt
import pickle
from utils import *
from streamlit_extras.badges import badge
from sklearn.gaussian_process.kernels import RBF
import warnings

from sko.GA import GA
from sko.PSO import PSO
from sko.DE import DE
from sko.AFSA import AFSA
from sko.SA import SAFast

# import sys
from prettytable import PrettyTable

import scienceplots

from algorithm.TrAdaboostR2 import TrAdaboostR2
from algorithm.mobo import Mobo4mat



warnings.filterwarnings('ignore')

st.set_page_config(
        page_title="MLMD",
        page_icon="🍁",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items={
        })

sysmenu = '''
<style>
MainMenu {visibility:hidden;}
footer {visibility:hidden;}
'''

# https://icons.bootcss.com/
st.markdown(sysmenu,unsafe_allow_html=True)
# arrow-repeat
with st.sidebar:
    select_option = option_menu("MLMD", ["平台主页", "基础功能", "特征工程", "回归预测", "主动学习","迁移学习", "代理优化", "其他"],
                    icons=['house', 'clipboard-data', 'menu-button-wide','bezier2', 'arrow-repeat','subtract', 'app', 'microsoft'],
                    menu_icon="boxes", default_index=0)
if select_option == "平台主页":
    st.write('''![](https://user-images.githubusercontent.com/61132191/231174459-96d33cdf-9f6f-4296-ba9f-31d11056ef12.jpg?raw=true)''')

# st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([1,0.25,0.2,0.5])
    with col1:
        pass
        # st.write('''
        #     Check out [help document](https://mlmd.netlify.app/) for more information
        #     ''')
    with col2:
        st.write('[![](https://img.shields.io/badge/MLMD-Github-yellowgreen)](https://github.com/Jiaxuan-Ma/Machine-Learning-for-Material-Design)')
    with col3:
        badge(type="github", name="Jiaxuan-Ma/MLMD")
    with col4:
        st.write("")
    colored_header(label="材料设计的机器学习平台",description="Machine Learning for Material Design",color_name="violet-90")
    # st.write("## Machine Learning for Material Design")
    # st.write("## 材料的机器学习平台")
    st.markdown(
    '''
    The **MLMD** platform (**M**achine **L**earning for **M**aterial **D**esign) for Material or Engineering aims at utilizing general and frontier machine learning algrithm to accelerate the material design with no-programming. \n
    材料基因组工程理念的发展将会大幅度提高新材料的研发效率、缩短研发周期、降低研发成本、全面加速材料从设计到工程化应用的进程。
    因此**MLMD**旨在为材料试验科研人员提供快速上手，无编程的机器学习算法平台，致力于材料试验到材料设计的一体化。
    ''')
    colored_header(label="数据布局",description="only support `.csv` file",color_name="violet-90")

    st.write('''![](https://user-images.githubusercontent.com/61132191/231178382-aa223924-f1cb-4e0e-afa1-08c536111f3a.jpg?raw=true)''')
    
    # colored_header(label="致谢",description="",color_name="violet-90")
    # st.markdown(
    # '''
    # 国家科技部重点研发计划(No. 2022YFB3707803)
    
    # ''')

elif select_option == "基础功能":

    colored_header(label="数据可视化",description=" ",color_name="violet-90")
    file = st.file_uploader("Upload `.csv`file", type=['csv'], label_visibility="collapsed")
    if file is None:
        table = PrettyTable(['上传文件名称', '名称','数据说明'])
        table.add_row(['file_1','dataset','数据集'])
        st.write(table)
    if file is not None:
        df = pd.read_csv(file)
        # check NaN
        check_string_NaN(df)
        
        colored_header(label="数据信息",description=" ",color_name="violet-70")

        nrow = st.slider("rows", 1, len(df)-1, 5)
        df_nrow = df.head(nrow)
        st.write(df_nrow)

        colored_header(label="数据初步统计",description=" ",color_name="violet-30")

        st.write(df.describe())

        tmp_download_link = download_button(df.describe(), f'数据统计.csv', button_text='download')
        
        st.markdown(tmp_download_link, unsafe_allow_html=True)

        colored_header(label="特征变量和目标变量", description=" ",color_name="violet-70")
        
        target_num = st.number_input('目标变量数量', min_value=1, max_value=10, value=1)
        col_feature, col_target = st.columns(2)
        # features
        features = df.iloc[:,:-target_num]
        # targets
        targets = df.iloc[:,-target_num:]
        with col_feature:    
            st.write(features.head())
        with col_target:   
            st.write(targets.head())

        colored_header(label="特征变量统计分布", description=" ",color_name="violet-30")

        feature_selected_name = st.selectbox('选择特征变量',list(features))
    
        feature_selected_value = features[feature_selected_name]
        plot = customPlot()
        col1, col2 = st.columns([1,3])
        with col1:  
            with st.expander("绘图参数"):
                options_selected = [plot.set_title_fontsize(1),plot.set_label_fontsize(2),
                            plot.set_tick_fontsize(3),plot.set_legend_fontsize(4),plot.set_color('line color',6,5),plot.set_color('bin color',0,6)]
        with col2:
            plot.feature_hist_kde(options_selected,feature_selected_name,feature_selected_value)

        #=========== Targets visulization ==================

        colored_header(label="目标变量统计分布", description=" ",color_name="violet-30")

        target_selected_name = st.selectbox('选择目标变量',list(targets))

        target_selected_value = targets[target_selected_name]
        plot = customPlot()
        col1, col2 = st.columns([1,3])
        with col1:  
            with st.expander("绘图参数"):
                options_selected = [plot.set_title_fontsize(7),plot.set_label_fontsize(8),
                            plot.set_tick_fontsize(9),plot.set_legend_fontsize(10), plot.set_color('line color',6,11), plot.set_color('bin color',0,12)]
        with col2:
            plot.target_hist_kde(options_selected,target_selected_name,target_selected_value)

        #=========== Features analysis ==================

        colored_header(label="特征变量配方（合金成分）", description=" ",color_name="violet-30")

        feature_range_selected_name = st.slider('选择特征变量个数',1,len(features.columns), (1,2))
        min_feature_selected = feature_range_selected_name[0]-1
        max_feature_selected = feature_range_selected_name[1]
        feature_range_selected_value = features.iloc[:,min_feature_selected: max_feature_selected]
        data_by_feature_type = df.groupby(list(feature_range_selected_value))
        feature_type_data = create_data_with_group_and_counts(data_by_feature_type)
        IDs = [str(id_) for id_ in feature_type_data['ID']]
        Counts = feature_type_data['Count']
        col1, col2 = st.columns([1,3])
        with col1:  
            with st.expander("绘图参数"):
                options_selected = [plot.set_title_fontsize(13),plot.set_label_fontsize(14),
                            plot.set_tick_fontsize(15),plot.set_legend_fontsize(16),plot.set_color('bin color',0, 17)]
        with col2:
            plot.featureSets_statistics_hist(options_selected,IDs, Counts)

        colored_header(label="特征变量在数据集中的分布", description=" ",color_name="violet-30")
        feature_selected_name = st.selectbox('选择特征变量', list(features),1)
        feature_selected_value = features[feature_selected_name]
        col1, col2 = st.columns([1,3])
        with col1:  
            with st.expander("绘图参数"):
                options_selected = [plot.set_title_fontsize(18),plot.set_label_fontsize(19),
                            plot.set_tick_fontsize(20),plot.set_legend_fontsize(21), plot.set_color('bin color', 0, 22)]
        with col2:
            plot.feature_distribution(options_selected,feature_selected_name,feature_selected_value)

        colored_header(label="特征变量和目标变量关系", description=" ",color_name="violet-30")
        col1, col2 = st.columns([1,3])
        with col1:  
            with st.expander("绘图参数"):
                options_selected = [plot.set_title_fontsize(23),plot.set_label_fontsize(24),
                            plot.set_tick_fontsize(25),plot.set_legend_fontsize(26),plot.set_color('scatter color',0, 27),plot.set_color('line color',6,28)]
        with col2:
            plot.features_and_targets(options_selected,df, list(features), list(targets))
        
        # st.write("### Targets and Targets ")
        if targets.shape[1] != 1:
            colored_header(label="目标变量和目标变量关系", description=" ",color_name="violet-30")
            col1, col2 = st.columns([1,3])
            with col1:  
                with st.expander("绘图参数"):
                    options_selected = [plot.set_title_fontsize(29),plot.set_label_fontsize(30),
                                plot.set_tick_fontsize(31),plot.set_legend_fontsize(32),plot.set_color('scatter color',0, 33),plot.set_color('line color',6,34)]
            with col2:
                plot.targets_and_targets(options_selected,df, list(targets))
    st.write('---')

elif select_option == "特征工程":
    with st.sidebar:
        sub_option = option_menu(None, ["空值处理", "特征唯一值处理", "特征和特征相关性", "特征和目标相关性", "One-hot编码", "特征重要性"])

    if sub_option == "空值处理":
        colored_header(label="空值处理",description=" ",color_name="violet-90")
        file = st.file_uploader("Upload `.csv`file", type=['csv'], label_visibility="collapsed")
        if file is None:
            table = PrettyTable(['上传文件名称', '名称','数据说明'])
            table.add_row(['file_1','dataset','数据集'])
            st.write(table)
        if file is not None:
        # colored_header(label="数据信息",description=" ",color_name="violet-70")
        # with st.expander('数据信息'):
            df = pd.read_csv(file)
            # check NuLL 
            null_columns = df.columns[df.isnull().any()]
            if len(null_columns) == 0:
                st.error('No missing features!')
                st.stop()
                
            colored_header(label="数据信息", description=" ",color_name="violet-70")
            nrow = st.slider("rows", 1, len(df)-1, 5)
            df_nrow = df.head(nrow)
            st.write(df_nrow)

            colored_header(label="目标变量和特征变量",description=" ",color_name="violet-70")

            target_num = st.number_input('目标变量数量',  min_value=1, max_value=10, value=1)
            
            col_feature, col_target = st.columns(2)
            # features
            features = df.iloc[:,:-target_num]
            # targets
            targets = df.iloc[:,-target_num:]
            with col_feature:    
                st.write(features.head())
            with col_target:   
                st.write(targets.head())
        
            # sub_sub_option = option_menu(None, ["丢弃空值", "填充空值"])
            colored_header(label="选择方法",description=" ",color_name="violet-70")
            sub_sub_option = option_menu(None, ["丢弃空值", "填充空值"],
                    icons=['house',  "list-task"],
                    menu_icon="cast", default_index=0, orientation="horizontal")
            if sub_sub_option == "丢弃空值":
                fs = FeatureSelector(features, targets)
                missing_threshold = st.slider("丢弃阈值(空值占比)",0.001, 1.0, 0.5)
                fs.identify_missing(missing_threshold)
                fs.features_dropped_missing = fs.features.drop(columns=fs.ops['missing'])
                
                data = pd.concat([fs.features_dropped_missing, targets], axis=1)
                st.write(data)
                tmp_download_link = download_button(data, f'空值丢弃数据.csv', button_text='download')
                st.markdown(tmp_download_link, unsafe_allow_html=True)
                st.write('%d features with $\gt$ %0.2f missing threshold.\n' % (len(fs.ops['missing']), fs.missing_threshold))
                plot = customPlot()

                with st.expander('绘图'):
                    col1, col2 = st.columns([1,3])
                    with col1:
                        options_selected = [plot.set_title_fontsize(1),plot.set_label_fontsize(2),
                                    plot.set_tick_fontsize(3),plot.set_legend_fontsize(4),plot.set_color('bin color',19,5)]
                    with col2:
                        plot.feature_missing(options_selected, fs.record_missing, fs.missing_stats)
                st.write('---')
            if sub_sub_option == "填充空值":
                fs = FeatureSelector(features, targets)
                missing_feature_list = fs.features.columns[fs.features.isnull().any()].tolist()
                with st.container():
                    fill_method = st.selectbox('填充方法',('常值', '随机森林算法'))
                
                if fill_method == '常值':

                    missing_feature = st.multiselect('丢失值特征',missing_feature_list,missing_feature_list[-1])
                    
                    option_filled = st.selectbox('均值',('均值','常数','中位数','众数'))
                    if option_filled == '均值':
                        # fs.features[missing_feature] = fs.features[missing_feature].fillna(fs.features[missing_feature].mean())
                        imp = SimpleImputer(missing_values=np.nan,strategy= 'mean')

                        fs.features[missing_feature] = imp.fit_transform(fs.features[missing_feature])
                    elif option_filled == '常数':
                        # fs.features[missing_feature] = fs.features[missing_feature].fillna(0)
                        fill_value = st.number_input('输入数值')
                        imp = SimpleImputer(missing_values=np.nan, strategy= 'constant', fill_value = fill_value)
                        
                        fs.features[missing_feature] = imp.fit_transform(fs.features[missing_feature])
                    elif option_filled == '中位数':
                        # fs.features[missing_feature] = fs.features[missing_feature].fillna(0)
                        imp = SimpleImputer(missing_values=np.nan, strategy= 'median')
                        
                        fs.features[missing_feature] = imp.fit_transform(fs.features[missing_feature])
                    elif option_filled == '众数':

                        imp = SimpleImputer(missing_values=np.nan, strategy= 'most_frequent')
                        
                        fs.features[missing_feature] = imp.fit_transform(fs.features[missing_feature])  

                    data = pd.concat([fs.features, targets], axis=1)
                else:
                    with st.expander('超参数'):
                        num_estimators = st.number_input('number estimators',1, 10000, 100)
                        criterion = st.selectbox('criterion',('squared_error','absolute_error','friedman_mse','poisson'))
                        max_depth = st.number_input('max depth',1, 1000, 5)
                        min_samples_leaf = st.number_input('min samples leaf', 1, 1000, 5)
                        min_samples_split = st.number_input('min samples split', 1, 1000, 5)
                        random_state = st.checkbox('random state 1024',True)


                    option_filled = st.selectbox('均值',('均值','常数','中位数','众数'))
                    if option_filled == '均值':
                        feature_missing_reg = fs.features.copy()
                        null_columns = feature_missing_reg.columns[feature_missing_reg.isnull().any()] 
            
                        null_counts = feature_missing_reg.isnull().sum()[null_columns].sort_values() 
                        null_columns_ordered = null_counts.index.tolist() 
        
                        for i in null_columns_ordered:
        
                            df = feature_missing_reg
                            fillc = df[i]
            
                            df = pd.concat([df.iloc[:,df.columns != i], pd.DataFrame(targets)], axis=1)
                    
                            df_temp_fill = SimpleImputer(missing_values=np.nan,strategy= 'mean').fit_transform(df)

                            YTrain = fillc[fillc.notnull()]
                            YTest = fillc[fillc.isnull()]
                            XTrain = df_temp_fill[YTrain.index,:]
                            XTest = df_temp_fill[YTest.index,:]

                            rfc = RFR(n_estimators=num_estimators,criterion=criterion,max_depth=max_depth,min_samples_leaf=min_samples_leaf,
                                    min_samples_split=min_samples_split,random_state=random_state)

                            rfc = rfc.fit(XTrain, YTrain)
                            YPredict = rfc.predict(XTest)
            
                            feature_missing_reg.loc[feature_missing_reg[i].isnull(), i] = YPredict

                    elif option_filled == '常数':

                        fill_value = st.number_input('输入数值')
                        feature_missing_reg = fs.features.copy()
                        
                        null_columns = feature_missing_reg.columns[feature_missing_reg.isnull().any()] 
            
                        null_counts = feature_missing_reg.isnull().sum()[null_columns].sort_values() 
                        null_columns_ordered = null_counts.index.tolist() 
        
                        for i in null_columns_ordered:

                            df = feature_missing_reg
                            fillc = df[i]
            
                            df = pd.concat([df.iloc[:,df.columns != i], pd.DataFrame(targets)], axis=1)

                            df_temp_fill = SimpleImputer(missing_values=np.nan, strategy= 'constant', fill_value = fill_value).fit_transform(df)

                            YTrain = fillc[fillc.notnull()]
                            YTest = fillc[fillc.isnull()]
                            XTrain = df_temp_fill[YTrain.index,:]
                            XTest = df_temp_fill[YTest.index,:]

                            rfc = RFR(n_estimators=num_estimators,criterion=criterion,max_depth=max_depth,min_samples_leaf=min_samples_leaf,
                                    min_samples_split=min_samples_split,random_state=random_state)

                            rfc = rfc.fit(XTrain, YTrain)
                            YPredict = rfc.predict(XTest)

                            feature_missing_reg.loc[feature_missing_reg[i].isnull(), i] = YPredict
                        
                    elif option_filled == '中位数':
                        feature_missing_reg = fs.features.copy()
                    
                        null_columns = feature_missing_reg.columns[feature_missing_reg.isnull().any()] 
                
                        null_counts = feature_missing_reg.isnull().sum()[null_columns].sort_values() 
                        null_columns_ordered = null_counts.index.tolist() 

                        for i in null_columns_ordered:
        
                            df = feature_missing_reg
                            fillc = df[i]
                
                            df = pd.concat([df.iloc[:,df.columns != i], pd.DataFrame(targets)], axis=1)
        
                            df_temp_fill = SimpleImputer(missing_values=np.nan,strategy= 'median').fit_transform(df)

                            YTrain = fillc[fillc.notnull()]
                            YTest = fillc[fillc.isnull()]
                            XTrain = df_temp_fill[YTrain.index,:]
                            XTest = df_temp_fill[YTest.index,:]

                            rfc = RFR(n_estimators=num_estimators,criterion=criterion,max_depth=max_depth,min_samples_leaf=min_samples_leaf,
                                    min_samples_split=min_samples_split,random_state=random_state)

                            rfc = rfc.fit(XTrain, YTrain)
                            YPredict = rfc.predict(XTest)
        
                            feature_missing_reg.loc[feature_missing_reg[i].isnull(), i] = YPredict
            
                    elif option_filled == '众数':

                        feature_missing_reg = fs.features.copy()
                    
                        null_columns = feature_missing_reg.columns[feature_missing_reg.isnull().any()] 
                
                        null_counts = feature_missing_reg.isnull().sum()[null_columns].sort_values() 
                        null_columns_ordered = null_counts.index.tolist() 

                        for i in null_columns_ordered:

                            df = feature_missing_reg
                            fillc = df[i]
                
                            df = pd.concat([df.iloc[:,df.columns != i], pd.DataFrame(targets)], axis=1)
            
                            df_temp_fill = SimpleImputer(missing_values=np.nan,strategy= 'most_frequent').fit_transform(df)

                            YTrain = fillc[fillc.notnull()]
                            YTest = fillc[fillc.isnull()]
                            XTrain = df_temp_fill[YTrain.index,:]
                            XTest = df_temp_fill[YTest.index,:]

                            rfc = RFR(n_estimators=num_estimators,criterion=criterion,max_depth=max_depth,min_samples_leaf=min_samples_leaf,
                                    min_samples_split=min_samples_split,random_state=random_state)
                            rfc = rfc.fit(XTrain, YTrain)
                            YPredict = rfc.predict(XTest)
                            
                            feature_missing_reg.loc[feature_missing_reg[i].isnull(), i] = YPredict

                    data = pd.concat([feature_missing_reg, targets], axis=1)

                st.write(data)

                tmp_download_link = download_button(data, f'空值填充数据.csv', button_text='download')
                st.markdown(tmp_download_link, unsafe_allow_html=True)
                st.write('---')
    
    elif sub_option == "特征唯一值处理":
        colored_header(label="特征唯一值处理",description=" ",color_name="violet-90")
        file = st.file_uploader("Upload `.csv`file", type=['csv'], label_visibility="collapsed")
        if file is None:
            table = PrettyTable(['上传文件名称', '名称','数据说明'])
            table.add_row(['file_1','dataset','数据集'])
            st.write(table)
        if file is not None:
            colored_header(label="数据信息",description=" ",color_name="violet-70")

            df = pd.read_csv(file)
            # 检测缺失值
            check_string_NaN(df)

            nrow = st.slider("rows", 1, len(df)-1, 5)
            df_nrow = df.head(nrow)
            st.write(df_nrow)

            colored_header(label="特征变量和目标变量",description=" ",color_name="violet-70")

            target_num = st.number_input('目标变量数量',  min_value=1, max_value=10, value=1)
            
            col_feature, col_target = st.columns(2)
            
            # features
            features = df.iloc[:,:-target_num]
            # targets
            targets = df.iloc[:,-target_num:]
            with col_feature:    
                st.write(features.head())
            with col_target:   
                st.write(targets.head())

            colored_header(label="丢弃唯一值特征变量",description=" ",color_name="violet-70")
            fs = FeatureSelector(features, targets)
            plot = customPlot() 

            col1, col2 = st.columns([1,3])
            with col1:
                
                fs.identify_nunique()
                option_counts = st.slider('丢弃唯一值特征数量',0, int(fs.unique_stats.max())-1,1)
                st.write(fs.unique_stats)
            with col2:

                fs.identify_nunique(option_counts)
                fs.features_dropped_single = fs.features.drop(columns=fs.ops['single_unique'])
                data = pd.concat([fs.features_dropped_single, targets], axis=1)
                st.write(fs.features_dropped_single)
                
                tmp_download_link = download_button(data, f'丢弃唯一值特征数据.csv', button_text='download')
                st.markdown(tmp_download_link, unsafe_allow_html=True)
                st.write('%d features $\leq$  %d unique value.\n' % (len(fs.ops['single_unique']),option_counts))
    
            with st.expander('绘图'):
                col1, col2 = st.columns([1,3])
                with col1:
                    options_selected = [plot.set_title_fontsize(6),plot.set_label_fontsize(7),
                                plot.set_tick_fontsize(8),plot.set_legend_fontsize(9),plot.set_color('bin color',19,10)]
                with col2:
                    plot.feature_nunique(options_selected, fs.record_single_unique,fs.unique_stats)     
                
            st.write('---')

    elif sub_option == "特征和特征相关性":
        colored_header(label="特征和特征相关性",description=" ",color_name="violet-90")
        file = st.file_uploader("Upload `.csv`file", type=['csv'], label_visibility="collapsed")
        if file is None:
            table = PrettyTable(['上传文件名称', '名称','数据说明'])
            table.add_row(['file_1','dataset','数据集'])
            st.write(table)
        if file is not None:
            df = pd.read_csv(file)
            # 检测缺失值
            check_string_NaN(df)
            colored_header(label="数据信息", description=" ",color_name="violet-70")
            nrow = st.slider("rows", 1, len(df)-1, 5)
            df_nrow = df.head(nrow)
            st.write(df_nrow)

            colored_header(label="特征变量和目标变量",description=" ",color_name="violet-70")

            target_num = st.number_input('目标变量数量',  min_value=1, max_value=10, value=1)
            
            col_feature, col_target = st.columns(2)
            # features
            features = df.iloc[:,:-target_num]
            # targets
            targets = df.iloc[:,-target_num:]
            with col_feature:    
                st.write(features.head())
            with col_target:   
                st.write(targets.head())
        
            colored_header(label="丢弃双线性特征变量",description=" ",color_name="violet-30")
            fs = FeatureSelector(features, targets)
            plot = customPlot() 

            target_selected_option = st.selectbox('选择目标', list(fs.targets))
            target_selected = fs.targets[target_selected_option]

            col1, col2 = st.columns([1,3])
            with col1:
                corr_method = st.selectbox("相关性分析方法",["pearson","spearman","kendall"])
                correlation_threshold = st.slider("相关性阈值",0.001, 1.0, 0.9) # 0.52
                corr_matrix = pd.concat([fs.features, target_selected], axis=1).corr(corr_method)
                fs.identify_collinear(corr_matrix, correlation_threshold)
                fs.judge_drop_f_t_after_f_f([target_selected_option], corr_matrix)

                is_mask = st.selectbox('掩码',('Yes', 'No'))
                with st.expander('绘图参数'):
                    options_selected = [plot.set_title_fontsize(19),plot.set_label_fontsize(20),
                                        plot.set_tick_fontsize(21),plot.set_legend_fontsize(22)]
                with st.expander('丢弃的特征变量'):
                    st.write(fs.record_collinear)
            with col2:
                fs.features_dropped_collinear = fs.features.drop(columns=fs.ops['collinear'])
                assert fs.features_dropped_collinear.size != 0,'zero feature !' 
                corr_matrix_drop_collinear = fs.features_dropped_collinear.corr(corr_method)
                plot.corr_cofficient(options_selected, is_mask, corr_matrix_drop_collinear)
                with st.expander('处理之后的数据'):
                    data = pd.concat([fs.features_dropped_collinear, targets], axis=1)
                    st.write(data)
                    tmp_download_link = download_button(data, f'双线性特征变量处理数据.csv', button_text='download')
                    st.markdown(tmp_download_link, unsafe_allow_html=True)

    elif sub_option == "特征和目标相关性":
        colored_header(label="特征和目标相关性",description=" ",color_name="violet-90")
        file = st.file_uploader("Upload `.csv`file", type=['csv'], label_visibility="collapsed")
        if file is None:
            table = PrettyTable(['上传文件名称', '名称','数据说明'])
            table.add_row(['file_1','dataset','数据集'])
            st.write(table)
        if file is not None:
            df = pd.read_csv(file)
            # 检测缺失值
            check_string_NaN(df)
            colored_header(label="数据信息", description=" ",color_name="violet-70")
            nrow = st.slider("rows", 1, len(df)-1, 5)
            df_nrow = df.head(nrow)
            st.write(df_nrow)

            colored_header(label="特征变量和目标变量",description=" ",color_name="violet-70")

            target_num = st.number_input('目标变量数量',  min_value=1, max_value=10, value=1)
            
            col_feature, col_target = st.columns(2)
            
            # features
            features = df.iloc[:,:-target_num]
            # targets
            targets = df.iloc[:,-target_num:]
            with col_feature:    
                st.write(features.head())
            with col_target:   
                st.write(targets.head())
        
            colored_header(label="丢弃与目标的低相关性特征",description=" ",color_name="violet-70")
            fs = FeatureSelector(features, targets)
            plot = customPlot() 
            target_selected_option = st.selectbox('选择特征', list(fs.targets))
            col1, col2 = st.columns([1,3])
            
            with col1:  
                corr_method = st.selectbox("相关性分析方法",["pearson","spearman","kendall","MIR"], key=15)  
                if corr_method != "MIR":
                    option_dropped_threshold = st.slider('相关性阈值',0.0, 1.0,0.0)
                if corr_method == 'MIR':
                    options_seed = st.checkbox('random state 1024',True)
                with st.expander('绘图参数'):
                    options_selected = [plot.set_title_fontsize(11),plot.set_label_fontsize(12),
                        plot.set_tick_fontsize(13),plot.set_legend_fontsize(14),plot.set_color('bin color',19,16)]
                
            with col2:
                target_selected = fs.targets[target_selected_option]
                if corr_method != "MIR":
                    corr_matrix = pd.concat([fs.features, target_selected], axis=1).corr(corr_method).abs()

                    fs.judge_drop_f_t([target_selected_option], corr_matrix, option_dropped_threshold)
                    
                    fs.features_dropped_f_t = fs.features.drop(columns=fs.ops['f_t_low_corr'])
                    corr_f_t = pd.concat([fs.features_dropped_f_t, target_selected], axis=1).corr(corr_method)[target_selected_option][:-1]

                    plot.corr_feature_target(options_selected, corr_f_t)
                    with st.expander('处理之后的数据'):
                        data = pd.concat([fs.features_dropped_f_t, targets], axis=1)
                        st.write(data)
                        tmp_download_link = download_button(data, f'丢弃与目标的低相关性特征数据.csv', button_text='download')
                        st.markdown(tmp_download_link, unsafe_allow_html=True)
                else:
                    if options_seed:
                        corr_mir  = MIR(fs.features, target_selected, random_state=1024)
                    else:
                        corr_mir = MIR(fs.features, target_selected)
                    corr_mir = pd.DataFrame(corr_mir).set_index(pd.Index(list(fs.features.columns)))
                    corr_mir.rename(columns={0: 'mutual info'}, inplace=True)
                    plot.corr_feature_target_mir(options_selected, corr_mir)
            st.write('---')

    elif sub_option == "One-hot编码":
        colored_header(label="One-hot编码",description=" ",color_name="violet-90")
        file = st.file_uploader("Upload `.csv`file", type=['csv'], label_visibility="collapsed")
        if file is None:
            table = PrettyTable(['上传文件名称', '名称','数据说明'])
            table.add_row(['file_1','dataset','数据集'])
            st.write(table)
        if file is not None:
            df = pd.read_csv(file)
            # 检测缺失值
            check_string_NaN(df)
            colored_header(label="数据信息", description=" ",color_name="violet-70")
            nrow = st.slider("rows", 1, len(df)-1, 5)
            df_nrow = df.head(nrow)
            st.write(df_nrow)

            colored_header(label="特征变量和目标变量",description=" ",color_name="violet-70")

            target_num = st.number_input('目标变量数量',  min_value=1, max_value=10, value=1)
            
            col_feature, col_target = st.columns(2)
            
            # features
            features = df.iloc[:,:-target_num]
            # targets
            targets = df.iloc[:,-target_num:]
            with col_feature:    
                st.write(features.head())
            with col_target:   
                st.write(targets.head())
        
        #=============== drop major missing features ================
    
            colored_header(label="特征变量one-hot编码",description=" ",color_name="violet-70")
            fs = FeatureSelector(features, targets)
            plot = customPlot() 
            str_col_list = fs.features.select_dtypes(include=['object']).columns.tolist()
            fs.one_hot_feature_encoder(True)
            data = pd.concat([fs.features_plus_oneHot, targets], axis=1)
            # delete origin string columns
            data = data.drop(str_col_list, axis=1)
            st.write(data)
            tmp_download_link = download_button(data, f'特征变量one-hot编码数据.csv', button_text='download')
            st.markdown(tmp_download_link, unsafe_allow_html=True)
            st.write('---')
    
    elif sub_option == "特征重要性":
        colored_header(label="特征重要性",description=" ",color_name="violet-90")
        file = st.file_uploader("Upload `.csv`file", type=['csv'], label_visibility="collapsed")
        if file is None:
            table = PrettyTable(['上传文件名称', '名称','数据说明'])
            table.add_row(['file_1','dataset','数据集'])
            st.write(table)
        if file is not None:
            df = pd.read_csv(file)
            # 检测缺失值
            check_string_NaN(df)
            colored_header(label="数据信息", description=" ",color_name="violet-70")
            nrow = st.slider("rows", 1, len(df)-1, 5)
            df_nrow = df.head(nrow)
            st.write(df_nrow)

            colored_header(label="特征变量和目标变量",description=" ",color_name="violet-70")

            target_num = st.number_input('目标变量数量',  min_value=1, max_value=10, value=1)
            
            col_feature, col_target = st.columns(2)        
            # features
            features = df.iloc[:,:-target_num]
            # targets
            targets = df.iloc[:,-target_num:]
            with col_feature:    
                st.write(features.head())
            with col_target:   
                st.write(targets.head())
    
            fs = FeatureSelector(features,targets)

            colored_header(label="选择目标变量", description=" ", color_name="violet-70")

            target_selected_name = st.selectbox('目标变量', list(fs.targets)[::-1])

            fs.targets = targets[target_selected_name]
            
            colored_header(label="Selector", description=" ",color_name="violet-70")

            model_path = './models/feature importance'
            
            template_alg = model_platform(model_path=model_path)

            colored_header(label="Training", description=" ",color_name="violet-70")

            inputs, col2 = template_alg.show()
            # st.write(inputs)

            if inputs['model'] == 'LinearRegressor':
                
                fs.model = LinearR()

                with col2:
                    option_cumulative_importance = st.slider('累计重要性阈值',0.0, 1.0, 0.95)
                    Embedded_method = st.checkbox('Embedded method',False)
                    if Embedded_method:
                        cv = st.number_input('cv',1,10,5)
                with st.container():
                    button_train = st.button('train', use_container_width=True)
                if button_train:
                    fs.LinearRegressor()     
                    fs.identify_zero_low_importance(option_cumulative_importance)
                    fs.feature_importance_select_show()
                    if Embedded_method:
                        threshold  = fs.cumulative_importance

                        feature_importances = fs.feature_importances.set_index('feature',drop = False)

                        features = []
                        scores = []
                        cumuImportance = []
                        for i in range(1, len(fs.features.columns) + 1):
                            features.append(feature_importances.iloc[:i, 0].values.tolist())
                            X_selected = fs.features[features[-1]]
                            score = CVS(fs.model, X_selected, fs.targets, cv=cv ,scoring='r2').mean()

                            cumuImportance.append(feature_importances.loc[features[-1][-1], 'cumulative_importance'])
                            scores.append(score)
                        cumu_importance = np.array(cumuImportance)
                        scores = np.array(scores) 
                        fig, ax = plt.subplots()
                        ax = plt.plot(cumu_importance, scores,'o-')
                        plt.xlabel("cumulative feature importance")
                        plt.ylabel("r2")
                        st.pyplot(fig)
            elif inputs['model'] == 'LassoRegressor':
                
                fs.model = Lasso(random_state=inputs['random state'])

                with col2:
                    option_cumulative_importance = st.slider('累计重要性阈值',0.0, 1.0, 0.95)
                    Embedded_method = st.checkbox('Embedded method',False)
                    if Embedded_method:
                        cv = st.number_input('cv',1,10,5)

                with st.container():
                    button_train = st.button('train', use_container_width=True)
                if button_train:

                    fs.LassoRegressor()

                    fs.identify_zero_low_importance(option_cumulative_importance)
                    fs.feature_importance_select_show()
                    if Embedded_method:
                        
                        threshold  = fs.cumulative_importance

                        feature_importances = fs.feature_importances.set_index('feature',drop = False)

                        features = []
                        scores = []
                        cumuImportance = []
                        for i in range(1, len(fs.features.columns) + 1):
                            features.append(feature_importances.iloc[:i, 0].values.tolist())
                            X_selected = fs.features[features[-1]]
                            score = CVS(fs.model, X_selected, fs.targets, cv=cv, scoring='r2').mean()

                            cumuImportance.append(feature_importances.loc[features[-1][-1], 'cumulative_importance'])
                            scores.append(score)
                        cumu_importance = np.array(cumuImportance)
                        scores = np.array(scores) 
                        fig, ax = plt.subplots()
                        ax = plt.plot(cumu_importance, scores,'o-')
                        plt.xlabel("cumulative feature importance")
                        plt.ylabel("r2")
                        st.pyplot(fig)

            elif inputs['model'] == 'RidgeRegressor':

                fs.model = Ridge(random_state=inputs['random state'])

                with col2:
                    option_cumulative_importance = st.slider('累计重要性阈值',0.0, 1.0, 0.95)
                    Embedded_method = st.checkbox('Embedded method',False)
                    if Embedded_method:
                        cv = st.number_input('cv',1,10,5)
                with st.container():
                    button_train = st.button('train', use_container_width=True)
                if button_train:
                    fs.RidgeRegressor()     
                    fs.identify_zero_low_importance(option_cumulative_importance)
                    fs.feature_importance_select_show()
                    if Embedded_method:
                        
                        threshold  = fs.cumulative_importance

                        feature_importances = fs.feature_importances.set_index('feature',drop = False)

                        features = []
                        scores = []
                        cumuImportance = []
                        for i in range(1, len(fs.features.columns) + 1):
                            features.append(feature_importances.iloc[:i, 0].values.tolist())
                            X_selected = fs.features[features[-1]]
                            score = CVS(fs.model, X_selected, fs.targets, cv=cv, scoring='r2').mean()

                            cumuImportance.append(feature_importances.loc[features[-1][-1], 'cumulative_importance'])
                            scores.append(score)
                        cumu_importance = np.array(cumuImportance)
                        scores = np.array(scores) 
                        fig, ax = plt.subplots()
                        ax = plt.plot(cumu_importance, scores,'o-')
                        plt.xlabel("cumulative feature importance")
                        plt.ylabel("r2")
                        st.pyplot(fig)
            elif inputs['model'] == 'LassoRegressor':
                
                fs.model = Lasso(random_state=inputs['random state'])

                with col2:
                    option_cumulative_importance = st.slider('累计重要性阈值',0.0, 1.0, 0.95)
                    Embedded_method = st.checkbox('Embedded method',False)
                    if Embedded_method:
                        cv = st.number_input('cv',1,10,5)
                with st.container():
                    button_train = st.button('train', use_container_width=True)
                if button_train:

                    fs.LassoRegressor()

                    fs.identify_zero_low_importance(option_cumulative_importance)
                    fs.feature_importance_select_show()
                    if Embedded_method:
                        
                        threshold  = fs.cumulative_importance

                        feature_importances = fs.feature_importances.set_index('feature',drop = False)

                        features = []
                        scores = []
                        cumuImportance = []
                        for i in range(1, len(fs.features.columns) + 1):
                            features.append(feature_importances.iloc[:i, 0].values.tolist())
                            X_selected = fs.features[features[-1]]
                            score = CVS(fs.model, X_selected, fs.targets, cv=cv, scoring='r2').mean()

                            cumuImportance.append(feature_importances.loc[features[-1][-1], 'cumulative_importance'])
                            scores.append(score)
                        cumu_importance = np.array(cumuImportance)
                        scores = np.array(scores) 
                        fig, ax = plt.subplots()
                        ax = plt.plot(cumu_importance, scores,'o-')
                        plt.xlabel("cumulative feature importance")
                        plt.ylabel("r2")
                        st.pyplot(fig)

            elif inputs['model'] == 'RandomForestRegressor':
                        
                        fs.model = RFR(criterion = inputs['criterion'], n_estimators=inputs['nestimators'] ,random_state=inputs['random state'],max_depth=inputs['max depth'],min_samples_leaf=inputs['min samples leaf'],
                                                        min_samples_split=inputs['min samples split'],oob_score=inputs['oob score'], warm_start=inputs['warm start'],
                                                        n_jobs=inputs['njobs'])
                        with col2:
                            option_cumulative_importance = st.slider('累计重要性阈值',0.5, 1.0, 0.95)
                            Embedded_method = st.checkbox('Embedded method',False)
                            if Embedded_method:
                                cv = st.number_input('cv',1,10,5)
                            
                        with st.container():
                            button_train = st.button('train', use_container_width=True)
                        if button_train:

                            fs.RandomForestRegressor()

                            fs.identify_zero_low_importance(option_cumulative_importance)
                            fs.feature_importance_select_show()

                            if Embedded_method:
                                
                                threshold  = fs.cumulative_importance

                                feature_importances = fs.feature_importances.set_index('feature',drop = False)

                                features = []
                                scores = []
                                cumuImportance = []
                                for i in range(1, len(fs.features.columns) + 1):
                                    features.append(feature_importances.iloc[:i, 0].values.tolist())
                                    X_selected = fs.features[features[-1]]
                                    score = CVS(fs.model, X_selected, fs.targets, cv=cv ,scoring='r2').mean()

                                    cumuImportance.append(feature_importances.loc[features[-1][-1], 'cumulative_importance'])
                                    scores.append(score)
                                cumu_importance = np.array(cumuImportance)
                                scores = np.array(scores) 
                                fig, ax = plt.subplots()
                                ax = plt.plot(cumu_importance, scores,'o-')
                                plt.xlabel("cumulative feature importance")
                                plt.ylabel("r2")
                                st.pyplot(fig)

            st.write('---')

elif select_option == "回归预测":

    colored_header(label="回归预测",description=" ",color_name="violet-90")
    file = st.file_uploader("Upload `.csv`file", type=['csv'], label_visibility="collapsed")
    if file is None:
        table = PrettyTable(['上传文件名称', '名称','数据说明'])
        table.add_row(['file_1','dataset','数据集'])
        st.write(table)
    if file is not None:
        df = pd.read_csv(file)
        # 检测缺失值
        check_string_NaN(df)

        colored_header(label="数据信息", description=" ",color_name="violet-70")
        nrow = st.slider("rows", 1, len(df)-1, 5)
        df_nrow = df.head(nrow)
        st.write(df_nrow)

        colored_header(label="特征变量和目标变量",description=" ",color_name="violet-70")

        target_num = st.number_input('目标变量数量',  min_value=1, max_value=10, value=1)
        
        col_feature, col_target = st.columns(2)
        # features
        features = df.iloc[:,:-target_num]
        # targets
        targets = df.iloc[:,-target_num:]
        with col_feature:    
            st.write(features.head())
        with col_target:   
            st.write(targets.head())
# =================== model ====================================
        reg = REGRESSOR(features,targets)

        colored_header(label="选择目标变量", description=" ", color_name="violet-70")

        target_selected_option = st.selectbox('target', list(reg.targets)[::-1])

        reg.targets = targets[target_selected_option]

        colored_header(label="Regressor", description=" ",color_name="violet-30")

        model_path = './models/regressors'

        template_alg = model_platform(model_path)

        inputs, col2 = template_alg.show()
    
        if inputs['model'] == 'DecisionTreeRegressor':

            with col2:
                with st.expander('Operator'):
                    operator = st.selectbox('', ('train test split','cross val score', 'leave one out'), label_visibility= "collapsed")
                    if operator == 'train test split':
                        inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                        reg.Xtrain, reg.Xtest, reg.Ytrain, reg.Ytest = TTS(reg.features,reg.targets,test_size=inputs['test size'],random_state=inputs['random state'])

                    elif operator == 'cross val score':
                        cv = st.number_input('cv',1,10,5)
                    
                    elif operator == 'leave one out':
                        loo = LeaveOneOut()
            
            colored_header(label="Training", description=" ",color_name="violet-30")
            with st.container():
                button_train = st.button('Train', use_container_width=True)
            if button_train:
                if operator == 'train test split':

                    reg.model = tree.DecisionTreeRegressor(random_state=inputs['random state'],splitter=inputs['splitter'],
                                    max_depth=inputs['max depth'],min_samples_leaf=inputs['min samples leaf'],
                                    min_samples_split=inputs['min samples split']) 
                    
                    reg.DecisionTreeRegressor()

                    result_data = pd.concat([reg.Ytest, pd.DataFrame(reg.Ypred)], axis=1)
                    result_data.columns = ['actual','prediction']
                    plot_and_export_results(reg, "DTR")

                    if inputs['tree graph']:
                        class_names = list(set(reg.targets.astype(str).tolist()))
                        dot_data = tree.export_graphviz(reg.model,out_file=None, feature_names=list(reg.features), class_names=class_names,filled=True, rounded=True)
                        graph = graphviz.Source(dot_data)
                        graph.render('Tree graph', view=True)

                elif operator == 'cross val score':

                    reg.model = tree.DecisionTreeRegressor(random_state=inputs['random state'],splitter=inputs['splitter'],
                        max_depth=inputs['max depth'],min_samples_leaf=inputs['min samples leaf'],
                        min_samples_split=inputs['min samples split']) 

                    cvs = CV(reg.model, reg.features, reg.targets, cv = cv, scoring=make_scorer(r2_score), return_train_score=False, return_estimator=True)
                    plot_cross_val_results(cvs, "DTR_cv")    

                elif operator == 'leave one out':

                    reg.model = tree.DecisionTreeRegressor(random_state=inputs['random state'],splitter=inputs['splitter'],
                        max_depth=inputs['max depth'],min_samples_leaf=inputs['min samples leaf'],
                        min_samples_split=inputs['min samples split']) 
                    
                    export_loo_results(reg, loo, "DTR_loo")



        if inputs['model'] == 'RandomForestRegressor':
            with col2:
                with st.expander('Operator'):
                    operator = st.selectbox('data operator', ('train test split','cross val score','leave one out','oob score'))
                    if operator == 'train test split':
                        inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                        reg.Xtrain, reg.Xtest, reg.Ytrain, reg.Ytest = TTS(reg.features,reg.targets,test_size=inputs['test size'],random_state=inputs['random state'])
                    elif operator == 'cross val score':
                        cv = st.number_input('cv',1,10,5)

                    elif operator == 'leave one out':
                        loo = LeaveOneOut()

                    elif operator == 'oob score':
                        inputs['oob score']  = st.selectbox('oob score',[True], disabled=True)
                        inputs['warm start'] = True

            colored_header(label="Training", description=" ",color_name="violet-30")
            with st.container():
                button_train = st.button('Train', use_container_width=True)
            
            if button_train:
                if operator == 'train test split':

                    reg.model = RFR( n_estimators=inputs['nestimators'] ,random_state=inputs['random state'],max_depth=inputs['max depth'],min_samples_leaf=inputs['min samples leaf'],
                                                    min_samples_split=inputs['min samples split'],oob_score=inputs['oob score'], warm_start=inputs['warm start'],
                                                    n_jobs=inputs['njobs'])
                    
                    reg.RandomForestRegressor()

                    result_data = pd.concat([reg.Ytest, pd.DataFrame(reg.Ypred)], axis=1)
                    result_data.columns = ['actual','prediction']
                    plot_and_export_results(reg, "RFR")


                elif operator == 'cross val score':

                    reg.model = RFR(n_estimators=inputs['nestimators'],random_state=inputs['random state'],max_depth=inputs['max depth'],min_samples_leaf=inputs['min samples leaf'],
                                                min_samples_split=inputs['min samples split'],oob_score=inputs['oob score'], warm_start=inputs['warm start'],
                                                n_jobs=inputs['njobs'])

                    cvs = CV(reg.model, reg.features, reg.targets, cv = cv, scoring=make_scorer(r2_score), return_train_score=False, return_estimator=True)
        
                    plot_cross_val_results(cvs, "RFR_cv") 
    
                elif operator == 'oob score':

                    reg.model = RFR(criterion = inputs['criterion'],n_estimators=inputs['nestimators'] ,random_state=inputs['random state'],max_depth=inputs['max depth'],min_samples_leaf=inputs['min samples leaf'],
                                                min_samples_split=inputs['min samples split'],oob_score=inputs['oob score'], warm_start=inputs['warm start'],
                                                n_jobs=inputs['njobs'])
                
                    reg_res  = reg.model.fit(reg.features, reg.targets)
                    oob_score = reg_res.oob_score_
                    st.write(f'oob score : {oob_score}')

                elif operator == 'leave one out':

                    reg.model = RFR(criterion = inputs['criterion'],n_estimators=inputs['nestimators'] ,random_state=inputs['random state'],max_depth=inputs['max depth'],min_samples_leaf=inputs['min samples leaf'],
                                                min_samples_split=inputs['min samples split'],oob_score=inputs['oob score'], warm_start=inputs['warm start'],
                                                n_jobs=inputs['njobs'])
                    export_loo_results(reg, loo, "RFR_loo")

        if inputs['model'] == 'SupportVector':

            with col2:
                with st.expander('Operator'):

                    preprocess = st.selectbox('data preprocess',['StandardScaler','MinMaxScaler'])

                    operator = st.selectbox('operator', ('train test split','cross val score', 'leave one out'), label_visibility='collapsed')
                    if operator == 'train test split':
                        inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                        if preprocess == 'StandardScaler':
                            reg.features = StandardScaler().fit_transform(reg.features)
                        if preprocess == 'MinMaxScaler':
                            reg.features = MinMaxScaler().fit_transform(reg.features)
                        
                        reg.features = pd.DataFrame(reg.features)    
                        
                        reg.Xtrain, reg.Xtest, reg.Ytrain, reg.Ytest = TTS(reg.features,reg.targets,test_size=inputs['test size'],random_state=inputs['random state'])

                    elif operator == 'cross val score':
                        if preprocess == 'StandardScaler':
                            reg.features = StandardScaler().fit_transform(reg.features)
                        if preprocess == 'MinMaxScaler':
                            reg.features = MinMaxScaler().fit_transform(reg.features)
                        cv = st.number_input('cv',1,10,5)

                    elif operator == 'leave one out':
                        if preprocess == 'StandardScaler':
                            reg.features = StandardScaler().fit_transform(reg.features)
                        if preprocess == 'MinMaxScaler':
                            reg.features = MinMaxScaler().fit_transform(reg.features)
                        loo = LeaveOneOut()
            colored_header(label="Training", description=" ",color_name="violet-30")
            with st.container():
                button_train = st.button('Train', use_container_width=True)
            if button_train:
                if operator == 'train test split':

                    reg.model = SVR(kernel=inputs['kernel'], C=inputs['C'])
                    
                    reg.SupportVector()

                    result_data = pd.concat([reg.Ytest, pd.DataFrame(reg.Ypred)], axis=1)
                    result_data.columns = ['actual','prediction']
                    
                    plot_and_export_results(reg, "SVR")

                elif operator == 'cross val score':

                    reg.model = SVR(kernel=inputs['kernel'], C=inputs['C'])

                    cvs = CV(reg.model, reg.features, reg.targets, cv = cv, scoring=make_scorer(r2_score), return_train_score=False, return_estimator=True)
                    plot_cross_val_results(cvs, "SVR_cv")  


                elif operator == 'leave one out':

                    reg.model = SVR(kernel=inputs['kernel'], C=inputs['C'])
                
                    export_loo_results(reg, loo, "SVR_loo")
                    
        if inputs['model'] == 'KNeighborsRegressor':

            with col2:
                with st.expander('Operator'):

                    preprocess = st.selectbox('data preprocess',['StandardScaler','MinMaxScaler'])

                    operator = st.selectbox('operator', ('train test split','cross val score', 'leave one out'), label_visibility='collapsed')
                    if operator == 'train test split':
                        inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                        if preprocess == 'StandardScaler':
                            reg.features = StandardScaler().fit_transform(reg.features)
                        if preprocess == 'MinMaxScaler':
                            reg.features = MinMaxScaler().fit_transform(reg.features)
                        
                        reg.features = pd.DataFrame(reg.features)    
                        
                        reg.Xtrain, reg.Xtest, reg.Ytrain, reg.Ytest = TTS(reg.features,reg.targets,test_size=inputs['test size'],random_state=inputs['random state'])
                        
                    elif operator == 'cross val score':
                        if preprocess == 'StandardScaler':
                            reg.features = StandardScaler().fit_transform(reg.features)
                        if preprocess == 'MinMaxScaler':
                            reg.features = MinMaxScaler().fit_transform(reg.features)
                        cv = st.number_input('cv',1,10,5)

                    elif operator == 'leave one out':
                        if preprocess == 'StandardScaler':
                            reg.features = StandardScaler().fit_transform(reg.features)
                        if preprocess == 'MinMaxScaler':
                            reg.features = MinMaxScaler().fit_transform(reg.features)
                        loo = LeaveOneOut()

            colored_header(label="Training", description=" ",color_name="violet-30")
            with st.container():
                button_train = st.button('Train', use_container_width=True)
            if button_train:
                if operator == 'train test split':

                    reg.model = KNeighborsRegressor(n_neighbors = inputs['n neighbors'])
                    
                    reg.KNeighborsRegressor()

                    result_data = pd.concat([reg.Ytest, pd.DataFrame(reg.Ypred)], axis=1)
                    result_data.columns = ['actual','prediction']
                    
                    plot_and_export_results(reg, "KNR")

                elif operator == 'cross val score':

                    reg.model = KNeighborsRegressor(n_neighbors = inputs['n neighbors'])

                    cvs = CV(reg.model, reg.features, reg.targets, cv = cv, scoring=make_scorer(r2_score), return_train_score=False, return_estimator=True)

                    plot_cross_val_results(cvs, "KNR_cv") 

                elif operator == 'leave one out':

                    reg.model = KNeighborsRegressor(n_neighbors = inputs['n neighbors'])
                
                    export_loo_results(reg, loo, "KNR_loo")

        if inputs['model'] == 'LinearRegressor':

            with col2:
                with st.expander('Operator'):

                    preprocess = st.selectbox('data preprocess',['StandardScaler','MinMaxScaler'])

                    operator = st.selectbox('operator', ('train test split','cross val score', 'leave one out'), label_visibility='collapsed')
                    if operator == 'train test split':
                        inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                        if preprocess == 'StandardScaler':
                            reg.features = StandardScaler().fit_transform(reg.features)
                        if preprocess == 'MinMaxScaler':
                            reg.features = MinMaxScaler().fit_transform(reg.features)
                        
                        reg.features = pd.DataFrame(reg.features)    
                        
                        reg.Xtrain, reg.Xtest, reg.Ytrain, reg.Ytest = TTS(reg.features,reg.targets,test_size=inputs['test size'],random_state=inputs['random state'])
                        
                    elif operator == 'cross val score':
                        if preprocess == 'StandardScaler':
                            reg.features = StandardScaler().fit_transform(reg.features)
                        if preprocess == 'MinMaxScaler':
                            reg.features = MinMaxScaler().fit_transform(reg.features)
                        cv = st.number_input('cv',1,10,5)
    
                    elif operator == 'leave one out':
                        if preprocess == 'StandardScaler':
                            reg.features = StandardScaler().fit_transform(reg.features)
                        if preprocess == 'MinMaxScaler':
                            reg.features = MinMaxScaler().fit_transform(reg.features)
                        loo = LeaveOneOut()

            colored_header(label="Training", description=" ",color_name="violet-30")
            with st.container():
                button_train = st.button('Train', use_container_width=True)
            if button_train:
                if operator == 'train test split':

                    reg.model = LinearR()
                    
                    reg.LinearRegressor()
                    # plot = customPlot()
                    # plot.pred_vs_actual(reg.Ytest, reg.Ypred)

                    result_data = pd.concat([reg.Ytest, pd.DataFrame(reg.Ypred)], axis=1)
                    result_data.columns = ['actual','prediction']
                    plot_and_export_results(reg, "LinearR")                     


                elif operator == 'cross val score':

                    reg.model = LinearR()

                    cvs = CV(reg.model, reg.features, reg.targets, cv = cv, scoring=make_scorer(r2_score), return_train_score=False, return_estimator=True)

                    plot_cross_val_results(cvs, "linearR_cv")    

                elif operator == 'leave one out':

                    reg.model = LinearR()
                    
                    export_loo_results(reg, loo, "LinearR_loo")
        
                                
        if inputs['model'] == 'LassoRegressor':

            with col2:
                with st.expander('Operator'):

                    preprocess = st.selectbox('data preprocess',['StandardScaler','MinMaxScaler'])

                    operator = st.selectbox('', ('train test split','cross val score', 'leave one out'), label_visibility='collapsed')
                    if operator == 'train test split':
                        inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                        if preprocess == 'StandardScaler':
                            reg.features = StandardScaler().fit_transform(reg.features)
                        if preprocess == 'MinMaxScaler':
                            reg.features = MinMaxScaler().fit_transform(reg.features)
                        
                        reg.features = pd.DataFrame(reg.features)    
                        
                        reg.Xtrain, reg.Xtest, reg.Ytrain, reg.Ytest = TTS(reg.features,reg.targets,test_size=inputs['test size'],random_state=inputs['random state'])
                        
                    elif operator == 'cross val score':
                        if preprocess == 'StandardScaler':
                            reg.features = StandardScaler().fit_transform(reg.features)
                        if preprocess == 'MinMaxScaler':
                            reg.features = MinMaxScaler().fit_transform(reg.features)
                        cv = st.number_input('cv',1,10,5)

                    elif operator == 'leave one out':
                        if preprocess == 'StandardScaler':
                            reg.features = StandardScaler().fit_transform(reg.features)
                        if preprocess == 'MinMaxScaler':
                            reg.features = MinMaxScaler().fit_transform(reg.features)
                        loo = LeaveOneOut()
            
            colored_header(label="Training", description=" ",color_name="violet-30")
            with st.container():
                button_train = st.button('Train', use_container_width=True)
            if button_train:
                if operator == 'train test split':

                    reg.model = Lasso(alpha=inputs['alpha'],random_state=inputs['random state'])
                    
                    reg.LassoRegressor()

                    result_data = pd.concat([reg.Ytest, pd.DataFrame(reg.Ypred)], axis=1)
                    result_data.columns = ['actual','prediction']
                    
                    plot_and_export_results(reg, "LassoR")

                elif operator == 'cross val score':

                    reg.model = Lasso(alpha=inputs['alpha'],random_state=inputs['random state'])

                    cvs = CV(reg.model, reg.features, reg.targets, cv = cv, scoring=make_scorer(r2_score), return_train_score=False, return_estimator=True)

                    plot_cross_val_results(cvs, "LassoR_cv")   

                elif operator == 'leave one out':

                    reg.model = Lasso(alpha=inputs['alpha'],random_state=inputs['random state'])
                
                    export_loo_results(reg, loo, "LassoR_loo")

        if inputs['model'] == 'RidgeRegressor':

            with col2:
                with st.expander('Operator'):

                    preprocess = st.selectbox('data preprocess',['StandardScaler','MinMaxScaler'])

                    operator = st.selectbox('data operator', ('train test split','cross val score', 'leave one out'))
                    if operator == 'train test split':
                        inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                        if preprocess == 'StandardScaler':
                            reg.features = StandardScaler().fit_transform(reg.features)
                        if preprocess == 'MinMaxScaler':
                            reg.features = MinMaxScaler().fit_transform(reg.features)
                        
                        reg.features = pd.DataFrame(reg.features)    
                        
                        reg.Xtrain, reg.Xtest, reg.Ytrain, reg.Ytest = TTS(reg.features,reg.targets,test_size=inputs['test size'],random_state=inputs['random state'])
                        
                    elif operator == 'cross val score':
                        if preprocess == 'StandardScaler':
                            reg.features = StandardScaler().fit_transform(reg.features)
                        if preprocess == 'MinMaxScaler':
                            reg.features = MinMaxScaler().fit_transform(reg.features)
                        cv = st.number_input('cv',1,10,5)
                    
                    elif operator == 'leave one out':
                        if preprocess == 'StandardScaler':
                            reg.features = StandardScaler().fit_transform(reg.features)
                        if preprocess == 'MinMaxScaler':
                            reg.features = MinMaxScaler().fit_transform(reg.features)
                        loo = LeaveOneOut()              
            
            colored_header(label="Training", description=" ",color_name="violet-30")
            with st.container():
                button_train = st.button('Train', use_container_width=True)
            if button_train:
                if operator == 'train test split':

                    reg.model = Ridge(alpha=inputs['alpha'], random_state=inputs['random state'])
                    
                    reg.RidgeRegressor()

                    result_data = pd.concat([reg.Ytest, pd.DataFrame(reg.Ypred)], axis=1)
                    result_data.columns = ['actual','prediction']

                    plot_and_export_results(reg, "RidgeR")

                elif operator == 'cross val score':

                    reg.model = Ridge(alpha=inputs['alpha'], random_state=inputs['random state'])

                    cvs = CV(reg.model, reg.features, reg.targets, cv = cv, scoring=make_scorer(r2_score), return_train_score=False, return_estimator=True)

                    plot_cross_val_results(cvs, "LassoR_cv") 


                elif operator == 'leave one out':

                    reg.model = Ridge(alpha=inputs['alpha'], random_state=inputs['random state'])
                
                    export_loo_results(reg, loo, "LassoR_loo")

        if inputs['model'] == 'MLPRegressor':

            with col2:
                with st.expander('Operator'):

                    preprocess = st.selectbox('data preprocess',['StandardScaler','MinMaxScaler'])

                    operator = st.selectbox('operator', ('train test split','cross val score', 'leave one out'), label_visibility='collapsed')
                    if operator == 'train test split':
                        inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                        if preprocess == 'StandardScaler':
                            reg.features = StandardScaler().fit_transform(reg.features)
                        if preprocess == 'MinMaxScaler':
                            reg.features = MinMaxScaler().fit_transform(reg.features)
                        
                        reg.features = pd.DataFrame(reg.features)    
                        
                        reg.Xtrain, reg.Xtest, reg.Ytrain, reg.Ytest = TTS(reg.features,reg.targets,test_size=inputs['test size'],random_state=inputs['random state'])
                        
                    elif operator == 'cross val score':
                        if preprocess == 'StandardScaler':
                            reg.features = StandardScaler().fit_transform(reg.features)
                        if preprocess == 'MinMaxScaler':
                            reg.features = MinMaxScaler().fit_transform(reg.features)
                        cv = st.number_input('cv',1,10,5)
                    
                    elif operator == 'leave one out':
                        if preprocess == 'StandardScaler':
                            reg.features = StandardScaler().fit_transform(reg.features)
                        if preprocess == 'MinMaxScaler':
                            reg.features = MinMaxScaler().fit_transform(reg.features)
                        loo = LeaveOneOut()              
            colored_header(label="Training", description=" ",color_name="violet-30")
            with st.container():
                button_train = st.button('Train', use_container_width=True)
            if button_train:
                if operator == 'train test split':

                    reg.model = MLPRegressor(hidden_layer_sizes=inputs['hidden layer size'], activation= inputs['activation'], solver=inputs['solver'], 
                                            batch_size=inputs['batch size'], learning_rate= inputs['learning rate'], max_iter=inputs['max iter'],
                                            random_state=inputs['random state'])
                    reg.MLPRegressor()

                    result_data = pd.concat([reg.Ytest, pd.DataFrame(reg.Ypred)], axis=1)
                    result_data.columns = ['actual','prediction']
                    plot_and_export_results(reg, "MLP")

                elif operator == 'cross val score':

                    reg.model = MLPRegressor(hidden_layer_sizes=inputs['hidden layer size'], activation= inputs['activation'], solver=inputs['solver'], 
                                            batch_size=inputs['batch size'], learning_rate= inputs['learning rate'], max_iter=inputs['max iter'],
                                            random_state=inputs['random state'])
                    
                    cvs = CV(reg.model, reg.features, reg.targets, cv = cv, scoring=make_scorer(r2_score), return_train_score=False, return_estimator=True)
                    plot_cross_val_results(cvs, "MLP_cv") 

                elif operator == 'leave one out':

                    reg.model = MLPRegressor(hidden_layer_sizes=inputs['hidden layer size'], activation= inputs['activation'], solver=inputs['solver'], 
                                            batch_size=inputs['batch size'], learning_rate= inputs['learning rate'], max_iter=inputs['max iter'],
                                            random_state=inputs['random state'])
                
                    export_loo_results(reg, loo, "MLP_loo")

            st.write('---')
                            
elif select_option == "分类":
    
    file = st.file_uploader("Upload `.csv`file", type=['csv'], label_visibility="collapsed")
    if file is not None:
        df = pd.read_csv(file)
        # 检测缺失值
        check_string_NaN(df)
        colored_header(label="数据信息", description=" ",color_name="violet-70")
        nrow = st.slider("rows", 1, len(df)-1, 5)
        df_nrow = df.head(nrow)
        st.write(df_nrow)

        colored_header(label="特征变量和目标变量",description=" ",color_name="violet-70")

        target_num = st.number_input('目标变量数量',  min_value=1, max_value=10, value=1)
        
        col_feature, col_target = st.columns(2)
            
        # features
        features = df.iloc[:,:-target_num]
        # targets
        targets = df.iloc[:,-target_num:]
        with col_feature:    
            st.write(features.head())
        with col_target:   
            st.write(targets.head())
    
        clf = CLASSIFIER(features,targets)

        colored_header(label="Choose Target", description=" ", color_name="violet-30")
        target_selected_option = st.selectbox('target', list(clf.targets)[::-1])

        clf.targets = targets[target_selected_option]

        # st.write(fs.targets.head())
        colored_header(label="Classifier", description=" ",color_name="violet-30")

        model_path = './models/classifiers'
        
        template_alg = model_platform(model_path)

        colored_header(label="Training", description=" ",color_name="violet-30")

        inputs, col2 = template_alg.show()
       
        if inputs['model'] == 'DecisionTreeClassifier':

            with col2:
                with st.expander('Operator'):
                    data_process = st.selectbox('data process', ('train test split','cross val score'))
                    if data_process == 'train test split':
                        inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                        clf.Xtrain, clf.Xtest, clf.Ytrain, clf.Ytest = TTS(clf.features,clf.targets,test_size=inputs['test size'],random_state=inputs['random state'])
                    elif data_process == 'cross val score':
                        cv = st.number_input('cv',1,10,5)

            with st.container():
                button_train = st.button('Train', use_container_width=True)
            if button_train:
                if data_process == 'train test split':
                            
                    clf.model = tree.DecisionTreeClassifier(criterion=inputs['criterion'],random_state=inputs['random state'],splitter=inputs['splitter'],
                                                            max_depth=inputs['max depth'],min_samples_leaf=inputs['min samples leaf'],min_samples_split=inputs['min samples split'])
                                                               
                    clf.DecisionTreeClassifier()

                    plot = customPlot()
                    cm = confusion_matrix(y_true=clf.Ytest, y_pred=clf.Ypred)
                    plot.confusion_matrix(cm)
                    result_data = pd.concat([clf.Ytest, pd.DataFrame(clf.Ypred)], axis=1)
                    result_data.columns = ['actual','prediction']
                    with st.expander('Actual vs Predict'):
                        st.write(result_data)
                        tmp_download_link = download_button(result_data, f'prediction vs actual.csv', button_text='download')
                        st.markdown(tmp_download_link, unsafe_allow_html=True)
                    if inputs['tree graph']:
                        class_names = list(set(clf.targets.astype(str).tolist()))
                        dot_data = tree.export_graphviz(clf.model,out_file=None, feature_names=list(clf.features), class_names=class_names,filled=True, rounded=True)
                        graph = graphviz.Source(dot_data)
                        graph.render('Tree graph', view=True)
                elif data_process == 'cross val score':
                    clf.model = tree.DecisionTreeClassifier(criterion=inputs['criterion'],random_state=inputs['random state'],splitter=inputs['splitter'],
                                                            max_depth=inputs['max depth'],min_samples_leaf=inputs['min samples leaf'],min_samples_split=inputs['min samples split'])
                                                            
                    cvs = CVS(clf.model, clf.features, clf.targets, cv = cv)

                    st.write('cv mean accuracy score: {}'.format(cvs.mean())) 

        if inputs['model'] == 'RandomForestClassifier':
      
            with col2:
                with st.expander('Operator'):
                    data_process = st.selectbox('data process', ('train test split','cross val score','oob score'))
                    if data_process == 'train test split':
                        inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                        clf.Xtrain, clf.Xtest, clf.Ytrain, clf.Ytest = TTS(clf.features,clf.targets,test_size=inputs['test size'],random_state=inputs['random state'])
                    elif data_process == 'cross val score':
                        cv = st.number_input('cv',1,10,5)
             
                    elif data_process == 'oob score':
                        inputs['oob score']  = st.checkbox('oob score',True)
                        inputs['warm start'] = True
            with st.container():
                button_train = st.button('Train', use_container_width=True)
            if button_train:

                if data_process == 'train test split':

                    clf.model = RFC(criterion = inputs['criterion'],n_estimators=inputs['nestimators'],random_state=inputs['random state'],max_depth=inputs['max depth'],min_samples_leaf=inputs['min samples leaf'],
                                                min_samples_split=inputs['min samples split'], oob_score=inputs['oob score'], warm_start=inputs['warm start'])
                    
                    clf.RandomForestClassifier()
                    
                    plot = customPlot()
                    cm = confusion_matrix(y_true=clf.Ytest, y_pred=clf.Ypred)
                    plot.confusion_matrix(cm)

                    result_data = pd.concat([clf.Ytest, pd.DataFrame(clf.Ypred)], axis=1)
                    result_data.columns = ['actual','prediction']
                    with st.expander('Actual vs Predict'):
                        st.write(result_data)
                        tmp_download_link = download_button(result_data, f'prediction vs actual.csv', button_text='download')
                        st.markdown(tmp_download_link, unsafe_allow_html=True)        
                elif data_process == 'cross val score':

 
                    clf.model = RFC(criterion = inputs['criterion'],n_estimators=inputs['nestimators'],random_state=inputs['random state'],max_depth=inputs['max depth'],min_samples_leaf=inputs['min samples leaf'],
                                                min_samples_split=inputs['min samples split'], oob_score=inputs['oob score'], warm_start=inputs['warm start'])
                
     
                    cvs = CVS(clf.model, clf.features, clf.targets, cv = cv)
     
                    st.write('cv mean accuracy score: {}'.format(cvs.mean())) 

                elif data_process == 'oob score':
 
                    clf.model = RFC(criterion = inputs['criterion'],n_estimators=inputs['nestimators'] ,random_state=inputs['random state'],max_depth=inputs['max depth'],min_samples_leaf=inputs['min samples leaf'],
                                                min_samples_split=inputs['min samples split'], oob_score=inputs['oob score'], warm_start=inputs['warm start'])
                
                    clf_res  = clf.model.fit(clf.features, clf.targets)
                    oob_score = clf_res.oob_score_
                    st.write(f'oob score : {oob_score}')              


        if inputs['model'] == 'LogisticRegression':

            with col2:
                with st.expander('Operator'):
                      
                    preprocess = st.selectbox('data preprocess',['StandardScaler','MinMaxScaler'])
                    
                    data_process = st.selectbox('data process', ('train test split','cross val score'))
                    if data_process == 'train test split':
                        inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                        if preprocess == 'StandardScaler':
                            clf.features = StandardScaler().fit_transform(clf.features)
                        if preprocess == 'MinMaxScaler':
                            clf.features = MinMaxScaler().fit_transform(clf.features)
                        clf.Xtrain, clf.Xtest, clf.Ytrain, clf.Ytest = TTS(clf.features,clf.targets,test_size=inputs['test size'],random_state=inputs['random state'])
                        
                    elif data_process == 'cross val score':

                        if preprocess == 'StandardScaler':
                            clf.features = StandardScaler().fit_transform(clf.features)
                        if preprocess == 'MinMaxScaler':
                            clf.features = MinMaxScaler().fit_transform(clf.features)
                        cv = st.number_input('cv',1,10,5)
            with st.container():
                button_train = st.button('Train', use_container_width=True)
            
            if button_train:
                if data_process == 'train test split':
                            
                    clf.model = LR(penalty=inputs['penalty'],C=inputs['C'],solver=inputs['solver'],max_iter=inputs['max iter'],multi_class=inputs['multi class'],
                                   random_state=inputs['random state'],l1_ratio= inputs['l1 ratio'])   
                    clf.LogisticRegreesion()
                    
                    plot = customPlot()
                    cm = confusion_matrix(y_true=clf.Ytest, y_pred=clf.Ypred)
                    plot.confusion_matrix(cm)
                    result_data = pd.concat([clf.Ytest, pd.DataFrame(clf.Ypred)], axis=1)
                    result_data.columns = ['actual','prediction']
                    with st.expander('Actual vs Predict'):
                        st.write(result_data)
                        tmp_download_link = download_button(result_data, f'prediction vs actual.csv', button_text='download')
                        st.markdown(tmp_download_link, unsafe_allow_html=True)
                elif data_process == 'cross val score':
                    clf.model = LR(penalty=inputs['penalty'],C=inputs['C'],solver=inputs['solver'],max_iter=inputs['max iter'],multi_class=inputs['multi class'],
                                   random_state=inputs['random state'],l1_ratio= inputs['l1 ratio'])   
                     
                    cvs = CVS(clf.model, clf.features, clf.targets, cv = cv)

                    st.write('cv mean accuracy score: {}'.format(cvs.mean())) 

        if inputs['model'] == 'SupportVector':
            with col2:
                with st.expander('Operator'):
                    preprocess = st.selectbox('data preprocess',['StandardScaler','MinMaxScaler'])

                    data_process = st.selectbox('data process', ('train test split','cross val score'))
                    if data_process == 'train test split':
                        inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                        if preprocess == 'StandardScaler':
                            clf.features = StandardScaler().fit_transform(clf.features)
                        if preprocess == 'MinMaxScaler':
                            clf.features = MinMaxScaler().fit_transform(clf.features)
                        clf.Xtrain, clf.Xtest, clf.Ytrain, clf.Ytest = TTS(clf.features,clf.targets,test_size=inputs['test size'],random_state=inputs['random state'])

                    elif data_process == 'cross val score':
                        if preprocess == 'StandardScaler':
                            clf.features = StandardScaler().fit_transform(clf.features)
                        if preprocess == 'MinMaxScaler':
                            clf.features = MinMaxScaler().fit_transform(clf.features)
                        cv = st.number_input('cv',1,10,5)
   
            with st.container():
                button_train = st.button('Train', use_container_width=True)   
            if button_train:
                if data_process == 'train test split':
                            
                    clf.model = SVC(C=inputs['C'], kernel=inputs['kernel'], class_weight=inputs['class weight'])
                                                               
                    clf.SupportVector()
                    
                    plot = customPlot()
                    cm = confusion_matrix(y_true=clf.Ytest, y_pred=clf.Ypred)
                    plot.confusion_matrix(cm)
                    result_data = pd.concat([clf.Ytest, pd.DataFrame(clf.Ypred)], axis=1)
                    result_data.columns = ['actual','prediction']
                    with st.expander('Actual vs Predict'):
                        st.write(result_data)
                        tmp_download_link = download_button(result_data, f'prediction vs actual.csv', button_text='download')
                        st.markdown(tmp_download_link, unsafe_allow_html=True)

            
                elif data_process == 'cross val score':
                    clf.model = SVC(C=inputs['C'], kernel=inputs['kernel'], class_weight=inputs['class weight'])
                                                                                             
                    cvs = CVS(clf.model, clf.features, clf.targets, cv = cv)
                    st.write('cv mean accuracy score: {}'.format(cvs.mean()))     

        st.write('---')

elif select_option == "聚类":
    file = st.file_uploader("Upload `.csv`file", type=['csv'], label_visibility="collapsed")


    if file is not None:
        df = pd.read_csv(file)
        # 检测缺失值
        check_string_NaN(df)
        colored_header(label="数据信息", description=" ",color_name="violet-70")
        nrow = st.slider("rows", 1, len(df)-1, 5)
        df_nrow = df.head(nrow)
        st.write(df_nrow)

        colored_header(label="特征变量和目标变量",description=" ",color_name="violet-70")

        target_num = st.number_input('目标变量数量',  min_value=1, max_value=10, value=1)
        
        col_feature, col_target = st.columns(2)
            
        # features
        features = df.iloc[:,:-target_num]
        # targets
        targets = df.iloc[:,-target_num:]
        with col_feature:    
            st.write(features.head())
        with col_target:   
            st.write(targets.head())
        
       #=============== cluster ================

        colored_header(label="Cluster",description=" ",color_name="violet-70")
        cluster = CLUSTER(features, targets)

        # colored_header(label="Choose Target", description=" ", color_name="violet-30")
        # target_selected_option = st.selectbox('target', list(cluster.targets)[::-1])

        # cluster.targets = targets[target_selected_option]

        model_path = './models/cluster'

        colored_header(label="Training", description=" ",color_name="violet-30")

        template_alg = model_platform(model_path)

        inputs, col2 = template_alg.show()
    
        if inputs['model'] == 'K-means':

            with col2:
                pass

            with st.container():
                button_train = st.button('Train', use_container_width=True)
            if button_train:
                
                    cluster.model = KMeans(n_clusters=inputs['n clusters'], random_state = inputs['random state'])
                    
                    cluster.K_means()

                    clustered_df = pd.concat([cluster.features,pd.DataFrame(cluster.model.labels_)], axis=1)
                    
                    r_name='cluster label'
                    c_name=clustered_df.columns[-1]
                    
                    clustered_df.rename(columns={c_name:r_name},inplace=True)
                    st.write(clustered_df)
            
        st.write('---')   

elif select_option == "主动学习":
    with st.sidebar:
        sub_option = option_menu(None, ["单目标主动学习", "多目标主动学习"])
    
    if sub_option == "单目标主动学习":

        colored_header(label="单目标主动学习",description=" ",color_name="violet-70")

        file = st.file_uploader("Upload `.csv`file", type=['csv'], label_visibility="collapsed", accept_multiple_files=True)
        if len(file) == 0:
            table = PrettyTable(['上传文件名称', '名称','数据说明'])
            table.add_row(['file_1','dataset','数据集'])
            table.add_row(['file_2','visual data','虚拟采样点'])
            st.write(table)
            st.info("If only one dataset is uploaded, the range of virtual sampling points can be adjusted in the program based on a ratio of 0.8~1.2 relative to the size of each feature dimension.")
        if len(file) > 2:
            st.error('May uploaded two files, the first is the dataset, the second is the the virtual space sample point. if only upload dataset, the virtual space can be adjusted by variable ratio')
            st.stop()
        # if len(file) == 2:
        #     st.info('You have unpload two files, the first is the dataset, the second is the the vritual space sample point.')       
        if len(file) > 0:
            
            colored_header(label="数据信息",description=" ",color_name="violet-70")

            # with st.expander('Data Information'):
            df = pd.read_csv(file[0])
            if len(file) == 2:
                df_vs = pd.read_csv(file[1])
            check_string_NaN(df)

            nrow = st.slider("rows", 1, len(df)-1, 5)
            df_nrow = df.head(nrow)
            st.write(df_nrow)

            colored_header(label="特征变量和目标变量",description=" ",color_name="violet-70")

            target_num = st.number_input('目标变量数量',  min_value=1, max_value=10, value=1)
            
            col_feature, col_target = st.columns(2)
            
            # features
            features = df.iloc[:,:-target_num]
            # targets
            targets = df.iloc[:,-target_num:]
            with col_feature:    
                st.write(features.head())
            with col_target:   
                st.write(targets.head())

            sp = SAMPLING(features, targets)

            colored_header(label="选择目标变量", description=" ", color_name="violet-70")

            target_selected_option = st.selectbox('target', list(sp.targets))
            
            sp.targets = sp.targets[target_selected_option]
            
            colored_header(label="Sampling", description=" ",color_name="violet-70")

            model_path = './models/active learning'

            template_alg = model_platform(model_path)

            inputs, col2 = template_alg.show()

            if inputs['model'] == 'BayeSampling':

                with col2:
                    if len(file) == 2:
                        sp.vsfeatures = df_vs
                        st.info('You have upoaded the visual sample point file.')
                        feature_name = sp.features.columns.tolist()
                    else:
                        feature_name = sp.features.columns.tolist()
                        mm = MinMaxScaler()
                        mm.fit(sp.features)
                        data_min = mm.data_min_
                        data_max = mm.data_max_
                        sp.trans_features = mm.transform(sp.features)
                        min_ratio, max_ratio = st.slider('sample space ratio', 0.8, 1.2, (1.0, 1.0))
            
                        sample_num = st.selectbox('sample number', ['10','20','50','80','100'])
                        feature_num = sp.trans_features.shape[1]

                        vs = np.linspace(min_ratio * data_min, max_ratio *data_max, int(sample_num))  

                        sp.vsfeatures = pd.DataFrame(vs, columns=feature_name)
                
                with st.expander('visual samples'):
                    st.write(sp.vsfeatures)
                    tmp_download_link = download_button(sp.vsfeatures, f'visual samples.csv', button_text='download')
                    st.markdown(tmp_download_link, unsafe_allow_html=True)
                Bgolearn = BGOS.Bgolearn()
                
                colored_header(label="Optimize", description=" ",color_name="violet-70")
                with st.container():
                    button_train = st.button('Train', use_container_width=True)
                if button_train:
                    Mymodel = Bgolearn.fit(data_matrix = sp.features, Measured_response = sp.targets, virtual_samples = sp.vsfeatures,
                                        opt_num=inputs['opt num'], min_search=inputs['min search'], noise_std= float(inputs['noise std']))
                    if inputs['sample criterion'] == 'Expected Improvement algorith':
                        res = Mymodel.EI()
                        
                    elif inputs['sample criterion'] == 'Expected improvement with "plugin"':
                        res = Mymodel.EI_plugin()

                    elif inputs['sample criterion'] == 'Augmented Expected Improvement':
                        with st.expander('EI HyperParamters'):
                            alpha = st.slider('alpha', 0.0, 3.0, 1.0)
                            tao = st.slider('tao',0.0, 1.0, 0.0)
                        res = Mymodel.Augmented_EI(alpha = alpha, tao = tao)

                    elif inputs['sample criterion'] == 'Expected Quantile Improvement':
                        with st.expander('EQI HyperParamters'):
                            beta= st.slider('beta',0.2, 0.8, 0.5)
                            tao = st.slider('tao_new',0.0, 1.0, 0.0)            
                        res = Mymodel.EQI(beta = beta,tao_new = tao)

                    elif inputs['sample criterion'] == 'Reinterpolation Expected Improvement':  
                        res = Mymodel.Reinterpolation_EI() 

                    elif inputs['sample criterion'] == 'Upper confidence bound':
                        with st.expander('UCB HyperParamters'):
                            alpha = st.slider('alpha', 0.0, 3.0, 1.0)
                        res = Mymodel.UCB(alpha=alpha)

                    elif inputs['sample criterion'] == 'Probability of Improvement':
                        with st.expander('PoI HyperParamters'):
                            tao = st.slider('tao',0.0, 0.3, 0.0)
                        res = Mymodel.PoI(tao = tao)

                    elif inputs['sample criterion'] == 'Predictive Entropy Search':
                        with st.expander('PES HyperParamters'):
                            sam_num = st.number_input('sample number',100, 1000, 500)
                        res = Mymodel.PES(sam_num = sam_num)  
                        
                    elif inputs['sample criterion'] == 'Knowledge Gradient':
                        with st.expander('Knowldge_G Hyperparameters'):
                            MC_num = st.number_input('MC number', 50,300,50)
                        res = Mymodel.Knowledge_G(MC_num = MC_num) 

                    elif inputs['sample criterion'] == 'Least Confidence':
                        
                        Mymodel = Bgolearn.fit(Mission='Classification', Classifier=inputs['Classifier'], data_matrix = sp.features, Measured_response = sp.targets, virtual_samples = sp.vsfeatures,
                                        opt_num=inputs['opt num'])
                        res = Mymodel.Least_cfd() 
        
                    elif inputs['sample criterion'] == 'Margin Sampling':
                        Mymodel = Bgolearn.fit(Mission='Classification', Classifier=inputs['Classifier'], data_matrix = sp.features, Measured_response = sp.targets, virtual_samples = sp.vsfeatures,
                                opt_num=inputs['opt num'])
                        res = Mymodel.Margin_S()

                    elif inputs['sample criterion'] == 'Entropy-based approach':
                        Mymodel = Bgolearn.fit(Mission='Classification', Classifier=inputs['Classifier'], data_matrix = sp.features, Measured_response = sp.targets, virtual_samples = sp.vsfeatures,
                                opt_num=inputs['opt num'])
                        res = Mymodel.Entropy()

                    st.info('Recommmended Sample')
                    sp.sample_point = pd.DataFrame(res[1], columns=feature_name)
                    st.write(sp.sample_point)
                    tmp_download_link = download_button(sp.sample_point, f'recommended samples.csv', button_text='download')
                    st.markdown(tmp_download_link, unsafe_allow_html=True)

    elif sub_option == "多目标主动学习":

        colored_header(label="多目标主动学习",description=" ",color_name="violet-70")
        file = st.file_uploader("Upload `.csv`file", type=['csv'], label_visibility="collapsed", accept_multiple_files=True)
        if len(file) == 0:
            table = PrettyTable(['上传文件名称', '名称','数据说明'])
            table.add_row(['file_1','dataset','数据集'])
            table.add_row(['file_2','visual data','虚拟采样点'])
            st.write(table)
            st.info("If only one dataset is uploaded, the range of virtual sampling points can be adjusted in the program based on a ratio of 0.8~1.2 relative to the size of each feature dimension.")
        if len(file) > 2:
            st.error('May upload two files, the first is the dataset, the second is the the virtual space sample point. if only upload dataset, the virtual space can be adjusted by variable ratio')
            st.stop() 
        if len(file) > 0:
            
            colored_header(label="数据信息",description=" ",color_name="violet-70")

            # with st.expander('Data Information'):
            df = pd.read_csv(file[0])
            if len(file) == 2:
                df_vs = pd.read_csv(file[1])
                check_string_NaN(df_vs)
            check_string_NaN(df)

            nrow = st.slider("rows", 1, len(df)-1, 5, key=1)
            df_nrow = df.head(nrow)
            st.write(df_nrow)

            colored_header(label="数据信息", description=" ",color_name="violet-70")
            nrow = st.slider("rows", 1, len(df)-1, 5)
            df_nrow = df.head(nrow)
            st.write(df_nrow)
            colored_header(label="特征变量和目标变量",description=" ",color_name="violet-70")

            target_num = st.number_input('目标变量数量',  min_value=1, max_value=10, value=2)
            
            col_feature, col_target = st.columns(2)
            # features
            features = df.iloc[:,:-target_num]
            # targets
            targets = df.iloc[:,-target_num:]
            with col_feature:    
                st.write(features.head())
            with col_target:   
                st.write(targets.head())
            
            col_feature, col_target = st.columns(2)

    # =================== model ====================================
            reg = REGRESSOR(features,targets)

            colored_header(label="选择目标变量", description=" ", color_name="violet-70")
            target_selected_option = st.multiselect('target', list(reg.targets)[::-1], default=targets.columns.tolist())
            
            reg.targets = targets[target_selected_option]
            reg.Xtrain = features
            reg.Ytrain = targets

            colored_header(label="Sampling", description=" ",color_name="violet-30")
            model_path = './models/multi-obj'

            template_alg = model_platform(model_path)
            inputs, col2 = template_alg.show()  

            if inputs['model'] == 'MOBO':

                with col2:
                    if len(file) == 2:
                        # features
                        vs_features = df_vs.iloc[:,:-target_num]
                        # targets
                        vs_targets = df_vs.iloc[:,-target_num:]
                        reg.Xtest = vs_features
                        st.info('You have upoaded the visual sample point file.')
                    else:
                        feature_name = features.columns.tolist()
                        mm = MinMaxScaler()
                        mm.fit(features)
                        data_min = mm.data_min_
                        data_max = mm.data_max_
                        trans_features = mm.transform(features)
                        min_ratio, max_ratio = st.slider('sample space ratio', 0.8, 1.2, (1.0, 1.0))
            
                        sample_num = st.selectbox('sample number', ['10','20','50','80','100'])
                        feature_num = trans_features.shape[1]

                        vs = np.linspace(min_ratio * data_min, max_ratio *data_max, int(sample_num))  
                        reg.Xtest = pd.DataFrame(vs, columns=feature_name)

                with st.expander('visual samples'):
                    st.write(reg.Xtest)
                    tmp_download_link = download_button(reg.Xtest, f'visual samples.csv', button_text='download')
                    st.markdown(tmp_download_link, unsafe_allow_html=True)
    
                pareto_front = find_non_dominated_solutions(reg.targets.values, target_selected_option)
                pareto_front = pd.DataFrame(pareto_front, columns=target_selected_option)
  
                if inputs['objective'] == 'max':  
                    # st.write(type(reg.targets.values))  
                    reg.targets = - reg.targets
                    pareto_front = find_non_dominated_solutions(reg.targets.values, target_selected_option)
                    pareto_front = pd.DataFrame(pareto_front, columns=target_selected_option)
                    pareto_front = -pareto_front
                    reg.targets = -reg.targets
                # st.write('pareto front of train data:', pareto_front)
                col1, col2 = st.columns([2, 1])
                with col1:
                    with plt.style.context(['nature','no-latex']):
                        fig, ax = plt.subplots()
                        ax.plot(pareto_front[target_selected_option[0]], pareto_front[target_selected_option[1]], 'k--')
                        ax.scatter(reg.targets[target_selected_option[0]], reg.targets[target_selected_option[1]])
                        ax.set_xlabel(target_selected_option[0])
                        ax.set_ylabel(target_selected_option[1])
                        ax.set_title('Pareto front of visual space')
                        st.pyplot(fig)
                with col2:
                    st.write(pareto_front)
                ref_point = []
                for i in range(len(target_selected_option)):
                    ref_point_loc = st.number_input(target_selected_option[i] + ' ref location', 0, 100000, 50)
                    ref_point.append(ref_point_loc)
                colored_header(label="Optimize", description=" ",color_name="violet-70")
                with st.container():
                    button_train = st.button('Opt', use_container_width=True)  
                if button_train:        
                    mobo = Mobo4mat()
                    row_train = reg.Xtrain.shape[0]
                    row_test = reg.Xtest.shape[0]
                    if inputs['normalize'] == 'StandardScaler':
                        reg.data = pd.concat([reg.Xtrain, reg.Xtest], axis = 0)
                        reg.data, scaler = mobo.normalize(reg.data, normalize='StandardScaler')
                    elif inputs['normalize'] == 'MinMaxScaler':
                        reg.data = pd.concat([reg.Xtrain, reg.Xtest], axis = 0)
                        reg.data, scaler = mobo.normalize(reg.data, normalize='MinMaxScaler')  
                    else:
                        reg.data = pd.concat([reg.Xtrain, reg.Xtest], axis = 0)
                    reg.Xtrain = reg.data.iloc[:row_train]
                    reg.Xtest = reg.data.iloc[row_train:]

                    HV, recommend_point = mobo.fit(X = reg.Xtrain, y = reg.Ytrain, visual_data=reg.Xtest, method=inputs['method'],number= inputs['num'], objective=inputs['objective'], ref_point=ref_point)
                    st.write('The maximum value of HV:')
                    st.write(HV)
                    st.write('The recommended point is :')
                    if inputs['normalize'] == 'StandardScaler':
                        recommend_point = mobo.inverse_normalize(recommend_point, scaler,  normalize='StandardScaler')
                    elif inputs['normalize'] == 'MinMaxScaler':
                        recommend_point = mobo.inverse_normalize(recommend_point, scaler,  normalize='MinMaxScaler')  
                    else:
                        recommend_point = recommend_point

                    st.write(recommend_point)
                    tmp_download_link = download_button(recommend_point, f'recommended samples.csv', button_text='download')
                    st.markdown(tmp_download_link, unsafe_allow_html=True)

elif select_option == "迁移学习":
    with st.sidebar:
        sub_option = option_menu(None, ["Boosting", "Neural Network"])

    if sub_option == "Boosting":
        colored_header(label="基于boosting迁移学习",description=" ",color_name="violet-90")
        sub_sub_option = option_menu(None, ["样本迁移","特征迁移","参数迁移"],
                                icons=['list-task',  "list-task","list-task"],
                                menu_icon="cast", default_index=0, orientation="horizontal")
        file = st.file_uploader("Upload `.csv`file", type=['csv'], label_visibility="collapsed", accept_multiple_files=True)
        if len(file) < 3:
            table = PrettyTable(['上传文件名称', '名称','数据说明'])
            table.add_row(['file_1','test_data','无标签目标域数据'])
            table.add_row(['file_2','target_data','有标签目标域数据'])
            table.add_row(['file_3','source_data_1','1 源域数据'])
            table.add_row(['...','...','...'])
            table.add_row(['file_n','source_data_n','n 源域数据'])
            st.write(table)
        else:
            # if len(file) == 3:
            df_test = pd.read_csv(file[0])
            df_target = pd.read_csv(file[1])
            df_source = pd.read_csv(file[2])
            if len(file) > 3:
                df_test = pd.read_csv(file[0])
                df_target = pd.read_csv(file[1])
                source_files = file[2:]
                df = [pd.read_csv(f) for f in source_files]
                df_source = pd.concat(df, axis=0)

            colored_header(label="数据信息", description=" ",color_name="violet-70")

            # show target data

            nrow = st.slider("rows", 1, len(df_target)-1, 5)
            df_nrow = df_target.head(nrow)
            st.write(df_nrow)
            colored_header(label="特征变量和目标变量",description=" ",color_name="violet-70")

            target_num = st.number_input('目标变量数量',  min_value=1, max_value=10, value=1)
            
            col_feature, col_target = st.columns(2)
            # features
            target_features = df_target.iloc[:,:-target_num]
            source_features = df_source.iloc[:,:-target_num]
            
            # targets
            target_targets = df_target.iloc[:,-target_num:]
            source_targets = df_source.iloc[:,-target_num:]

            with col_feature:    
                st.write(target_features.head())
            with col_target:   
                st.write(target_targets.head())
    # =================== model ====================================
            # features = pd.concat([source_features, target_features], axis=0)
            # targets = pd.concat([source_targets,target_targets], axis=0)
            reg = REGRESSOR(target_features, target_targets)

            colored_header(label="选择目标变量", description=" ", color_name="violet-70")

            target_selected_option = st.selectbox('target', list(reg.targets)[::-1])

            reg.targets = target_targets[target_selected_option]

            colored_header(label="Transfer", description=" ",color_name="violet-30")

            model_path = './models/transfer learning'

            template_alg = model_platform(model_path)

            inputs, col2 = template_alg.show()
            # TrAdaBoostR2 = template_alg.TrAdaBoostR2(reg.)
            with col2:
                st.write('')
            
            # reg.model = tree.DecisionTreeRegressor(random_state=inputs['random state'],splitter=inputs['splitter'],
            #             max_depth=inputs['max depth'],min_samples_leaf=inputs['min samples leaf'],
            #             min_samples_split=inputs['min samples split']) 

            if inputs['model'] == 'TrAdaboostR2':
                TrAdaboostR2 = TrAdaboostR2()
                with st.container():
                    button_train = st.button('Train', use_container_width=True)

                if inputs['max iter'] > source_features.shape[0]:
                    st.warning('The maximum of iterations should be smaller than %d' % source_features.shape[0])
                st.warning('the regression result have to been modified in the latter')
                if button_train:
                    TrAdaboostR2.fit(inputs, source_features, target_features, source_targets[target_selected_option], target_targets[target_selected_option], inputs['max iter'])
                    
                    Xtest = df_test[list(target_features.columns)]
                    predict = TrAdaboostR2.estimators_predict(Xtest)
                    prediction = pd.DataFrame(predict, columns=[target_selected_option])
                    try:
                        Ytest = df_test[target_selected_option]
                        plot = customPlot()
                        plot.pred_vs_actual(Ytest, prediction)
                        r2 = r2_score(Ytest, prediction)
                        st.write('R2: {}'.format(r2))
                        result_data = pd.concat([Ytest, pd.DataFrame(prediction)], axis=1)
                        result_data.columns = ['actual','prediction']
                        with st.expander('预测结果'):
                            st.write(result_data)
                            tmp_download_link = download_button(result_data, f'预测结果.csv', button_text='download')
                            st.markdown(tmp_download_link, unsafe_allow_html=True)
                    except KeyError:
                        st.write(prediction)
                        tmp_download_link = download_button(prediction, f'预测结果.csv', button_text='download')
                        st.markdown(tmp_download_link, unsafe_allow_html=True)
            
            elif inputs['model'] == 'TwoStageTrAdaboostR2':
                st.write('Please wait...')
            elif inputs['model'] == 'TwoStageTrAdaboostR2-revised':
                st.write('Please wait...')
                st.write('---')

    elif sub_option == "Neural Network":
        colored_header(label="基于Neural Network迁移学习",description=" ",color_name="violet-90")
        sub_sub_option = option_menu(None, ["样本迁移","特征迁移","参数迁移"],
                                icons=['list-task',  "list-task","list-task"],
                                menu_icon="cast", default_index=0, orientation="horizontal")      

elif select_option == "代理优化":
    with st.sidebar:
        sub_option = option_menu(None, ["单目标代理优化", "多目标代理优化","迁移学习-单目标代理优化","迁移学习-多目标代理优化"])
    if sub_option == "单目标代理优化":

        colored_header(label="单目标代理优化",description=" ",color_name="violet-90")
        file = st.file_uploader("Upload `.pickle` model and `.csv` file",  label_visibility="collapsed", accept_multiple_files=True)
        if len(file) < 2:
            table = PrettyTable(['上传文件名称', '名称','数据说明'])
            table.add_row(['file_1','boundary','设计变量上下界'])
            table.add_row(['file_2','model','模型'])
            st.write(table)
            st.info('You need unpload two files, the first is the feature variable boundary, the second is the trained models.')       
        if len(file) >= 2:    
            model = pickle.load(file[1])
            model_path = './models/surrogate optimize'
            template_alg = model_platform(model_path)

            inputs, col2 = template_alg.show()
            df_var = pd.read_csv(file[0])
            features_name = df_var.columns.tolist()
            range_var = df_var.values
            vars_min = get_column_min(range_var)
            vars_max = get_column_max(range_var)
            inputs['lb'] = vars_min
            inputs['ub'] = vars_max

            if inputs['model'] == 'PSO':      
                with col2:
                    if not len(inputs['lb']) == len(inputs['ub']) == inputs['n dim']:
                        st.warning('the variable dim is not match')
                    else:
                        st.info('the variable dim is  %d' % inputs['n dim'])
                with st.container():
                    button_train = st.button('Opt', use_container_width=True)
                if button_train:  
                    def opt_func(x):
                        x = x.reshape(1,-1)
                        y_pred = model.predict(x)
                        return y_pred  
                    
                    alg = PSO(func=opt_func, dim=inputs['n dim'], pop=inputs['size pop'], max_iter=inputs['max iter'], lb=inputs['lb'], ub=inputs['ub'],
                            w=inputs['w'], c1=inputs['c1'], c2=inputs['c2'])
            
                    alg.run()

                    st.info('Recommmended Sample')
                    gbest_x = pd.DataFrame({'Feature':features_name, 'value': alg.gbest_x})
                    st.write(gbest_x)         
                    tmp_download_link = download_button(gbest_x, f'recommended samples.csv', button_text='download')
                    st.markdown(tmp_download_link, unsafe_allow_html=True)
                    st.info('gbest_y: %s' % alg.gbest_y.item())
            
            elif inputs['model'] == 'GA':
                with col2:
                    if not len(inputs['lb']) == len(inputs['ub']) == inputs['n dim']:
                        st.warning('the variable dim is not match')
                    else:
                        st.info('the variable dim is  %d' % inputs['n dim'])
                with st.container():
                    button_train = st.button('Opt', use_container_width=True)
                if button_train:  
                    def opt_func(x):
                        x = x.reshape(1,-1)
                        y_pred = model.predict(x)
                        return y_pred  

                    alg = GA(func=opt_func, n_dim=inputs['n dim'], size_pop=inputs['size pop'], max_iter=inputs['max iter'], lb=inputs['lb'], ub=inputs['ub'],
                            prob_mut = inputs['prob mut'])

                    best_x, best_y = alg.run()

                    st.info('Recommmended Sample')
                    gbest_x = pd.DataFrame({'Feature':features_name, 'value': best_x})
                    st.write(gbest_x)         
                    tmp_download_link = download_button(gbest_x, f'recommended samples.csv', button_text='download')
                    st.markdown(tmp_download_link, unsafe_allow_html=True)
                    st.info('gbest_y: %s' %  best_y.item())
                    

                    # demo_func = lambda x: (x[0] - 1) ** 2 + (x[1] - 0.05) ** 2 + x[2] ** 2
                    # ga = GA(func=demo_func, n_dim=3, max_iter=500, lb=[-1, -1, -1], ub=[5, 1, 1], precision=[2, 1, 1e-7])
                    # best_x, best_y = ga.run()
                    # st.write('best_x:', best_x, '\n', 'best_y:', best_y)

            elif inputs['model'] == 'DE':
                with col2:
                    if not len(inputs['lb']) == len(inputs['ub']) == inputs['n dim']:
                        st.warning('the variable dim is not match')
                    else:
                        st.info('the variable dim is  %d' % inputs['n dim'])
                with st.container():
                    button_train = st.button('Opt', use_container_width=True)
                if button_train:  
                    def opt_func(x):
                        x = x.reshape(1,-1)
                        y_pred = model.predict(x)
                        return y_pred  
                    
                    alg = DE(func=opt_func, n_dim=inputs['n dim'], size_pop=inputs['size pop'], max_iter=inputs['max iter'], lb=inputs['lb'], ub=inputs['ub'],
                            prob_mut = inputs['prob mut'], F=inputs['F'])

                    best_x, best_y = alg.run()

                    st.info('Recommmended Sample')
                    gbest_x = pd.DataFrame({'Feature':features_name, 'value': best_x})
                    st.write(gbest_x)         
                    tmp_download_link = download_button(gbest_x, f'recommended samples.csv', button_text='download')
                    st.markdown(tmp_download_link, unsafe_allow_html=True)
                    st.info('gbest_y: %s' %  best_y.item())   
            
            elif inputs['model'] == 'AFSA':
                with col2:
                    if not len(inputs['lb']) == len(inputs['ub']) == inputs['n dim']:
                        st.warning('the variable dim is not match')
                    else:
                        st.info('the variable dim is  %d' % inputs['n dim'])
                with st.container():
                    button_train = st.button('Opt', use_container_width=True)
                if button_train:  
                    def opt_func(x):
                        x = x.reshape(1,-1)
                        y_pred = model.predict(x)
                        return y_pred  
                    
                    alg = AFSA(func=opt_func, n_dim=inputs['n dim'], size_pop=inputs['size pop'], max_iter=inputs['max iter'],
                            max_try_num=inputs['max try num'], step=inputs['step'], visual=inputs['visual'], q=inputs['q'], delta=inputs['delta'])

                    best_x, best_y = alg.run()

                    st.info('Recommmended Sample')
                    gbest_x = pd.DataFrame({'Feature':features_name, 'value': best_x})
                    st.write(gbest_x)         
                    tmp_download_link = download_button(gbest_x, f'recommended samples.csv', button_text='download')
                    st.markdown(tmp_download_link, unsafe_allow_html=True)
                    st.info('gbest_y: %s' %  best_y.item())   
            
            elif inputs['model'] == 'SA':
                with col2:
                    if not len(inputs['lb']) == len(inputs['ub']) == inputs['n dim']:
                        st.warning('the variable dim is not match')
                    else:
                        st.info('the variable dim is  %d' % inputs['n dim'])
                with st.container():
                    button_train = st.button('Opt', use_container_width=True)
                if button_train:  
                    def opt_func(x):
                        x = x.reshape(1,-1)
                        y_pred = model.predict(x)
                        return y_pred  
                    x0 = calculate_mean(inputs['lb'], inputs['ub'])
                    # st.write(inputs['lb'])
                    # st.write(inputs['ub'])
                    # st.write('pppppppppppppp')
                    # st.write(x0)
                    alg = SAFast(func=opt_func, x0=x0, T_max = inputs['T max'], q=inputs['q'], L=inputs['L'], max_stay_counter=inputs['max stay counter'],
                                lb=inputs['lb'], ub=inputs['ub'])

                    best_x, best_y = alg.run()

                    st.info('Recommmended Sample')
                    gbest_x = pd.DataFrame({'Feature':features_name, 'value': best_x})
                    st.write(gbest_x)         
                    tmp_download_link = download_button(gbest_x, f'recommended samples.csv', button_text='download')
                    st.markdown(tmp_download_link, unsafe_allow_html=True)
                    st.info('gbest_y: %s' %  best_y.item())                   

    elif sub_option == "多目标代理优化":

        colored_header(label="多目标代理优化",description=" ",color_name="violet-90")
        file = st.file_uploader("Upload `.pickle` model and `.csv` file",  label_visibility="collapsed", accept_multiple_files=True)
        if len(file) < 3:
            table = PrettyTable(['上传文件名称', '名称','数据说明'])
            table.add_row(['file_1','boundary','设计变量上下界'])
            table.add_row(['file_2','model_1','目标1 模型'])
            table.add_row(['file_3','model_2','目标2 模型'])
            st.write(table)
            st.info('You need unpload three files, the first is the feature variable boundary, the second and the three are the trained models.')  
        if len(file) >= 3:      
            model_1 = pickle.load(file[1])
            model_2 = pickle.load(file[2])
            model_path = './models/surrogate optimize'
            template_alg = model_platform(model_path)

            inputs, col2 = template_alg.show()
            df_var = pd.read_csv(file[0])
            features_name = df_var.columns.tolist()
            range_var = df_var.values
            vars_min = get_column_min(range_var)
            vars_max = get_column_max(range_var)
            inputs['lb'] = vars_min
            inputs['ub'] = vars_max

    elif sub_option == "迁移学习-多目标代理优化":
        colored_header(label="迁移学习-多目标代理优化",description=" ",color_name="violet-90")
        file = st.file_uploader("Upload `.pickle` model and `.csv` file",  label_visibility="collapsed", accept_multiple_files=True)
        if len(file) < 5:
            table = PrettyTable(['上传文件名称', '名称','数据说明'])
            table.add_row(['file_1','boundary','设计变量上下界'])
            table.add_row(['file_2','boundary','目标1 学习器权重'])
            table.add_row(['file_3','boundary','目标2 学习器权重'])
            table.add_row(['file_4','model','目标1 模型1'])
            table.add_row(['file_5','model','目标2 模型2'])
            st.write(table)
            st.info('You need unpload multi files, the first is the feature variable boundary, the second and the three are the weight of models, the remains are models.')  
        if len(file) >= 5:
            pass
    elif sub_option == "迁移学习-单目标代理优化":
        colored_header(label="迁移学习-单目标代理优化",description=" ",color_name="violet-90")
        file = st.file_uploader("Upload `.pickle` model and `.csv` file",  label_visibility="collapsed", accept_multiple_files=True)
        if len(file) < 3:
            table = PrettyTable(['上传文件名称', '名称','数据说明'])
            table.add_row(['file_1','boundary','设计变量上下界'])
            table.add_row(['file_2','boundary','学习器权重'])
            table.add_row(['file_3','model','模型'])
            st.write(table)
            st.info('You need unpload multi files, the first is the feature variable boundary, the second is the weight of models, the three is the model.')  
        if len(file) >= 3:
            pass

elif select_option == "其他":
    with st.sidebar:
        sub_option = option_menu(None, [ "集成学习", "模型推理","可解释性机器学习"])
    if sub_option == "可解释性机器学习":
        colored_header(label="可解释性机器学习",description=" ",color_name="violet-90")

        file = st.file_uploader("Upload `.csv`file", type=['csv'], label_visibility="collapsed")
        if file is None:
            table = PrettyTable(['上传文件名称', '名称','数据说明'])
            table.add_row(['file_1','dataset','数据集'])
            st.write(table)        
        if file is not None:
            df = pd.read_csv(file)
            # 检测缺失值
            check_string_NaN(df)
            colored_header(label="数据信息", description=" ",color_name="violet-70")
            nrow = st.slider("rows", 1, len(df)-1, 5)
            df_nrow = df.head(nrow)
            st.write(df_nrow)

            colored_header(label="特征变量和目标变量",description=" ",color_name="violet-70")

            target_num = st.number_input('目标变量数量',  min_value=1, max_value=10, value=1)
            
            col_feature, col_target = st.columns(2)
                
            # features
            features = df.iloc[:,:-target_num]
            # targets
            targets = df.iloc[:,-target_num:]
            with col_feature:    
                st.write(features.head())
            with col_target:   
                st.write(targets.head())


            colored_header(label="Shapley value",description=" ",color_name="violet-70")

            fs = FeatureSelector(features, targets)

            target_selected_option = st.selectbox('choose target', list(fs.targets))
            fs.targets = fs.targets[target_selected_option]
            # regressor = st.selectbox('tree',['linear','kernel','sampling'])
            reg = RFR()
            X_train, X_test, y_train, y_test = TTS(fs.features, fs.targets, random_state=0) 
            test_size = st.slider('test size',0.1, 0.5, 0.2) 
            random_state = st.checkbox('random state 1024',True)
            if random_state:
                random_state = 1024
            else:
                random_state = None
                
            fs.Xtrain,fs.Xtest, fs.Ytrain, fs.Ytest = TTS(fs.features,fs.targets,test_size=test_size,random_state=random_state)
            reg.fit(fs.Xtrain, fs.Ytrain)

            explainer = shap.TreeExplainer(reg)
            
            shap_values = explainer(fs.features)

            colored_header(label="SHAP Feature Importance", description=" ",color_name="violet-30")
            nfeatures = st.slider("features", 2, fs.features.shape[1],fs.features.shape[1])
            st_shap(shap.plots.bar(shap_values, max_display=nfeatures))

            colored_header(label="SHAP Feature Cluster", description=" ",color_name="violet-30")
            clustering = shap.utils.hclust(fs.features, fs.targets)
            clustering_cutoff = st.slider('clustering cutoff', 0.0,1.0,0.5)
            nfeatures = st.slider("features", 2, fs.features.shape[1],fs.features.shape[1], key=2)
            st_shap(shap.plots.bar(shap_values, clustering=clustering, clustering_cutoff=clustering_cutoff, max_display=nfeatures))

            colored_header(label="SHAP Beeswarm", description=" ",color_name="violet-30")
            rank_option = st.selectbox('rank option',['max','mean'])
            max_dispaly = st.slider('max display',2, fs.features.shape[1],fs.features.shape[1])
            if rank_option == 'max':
                st_shap(shap.plots.beeswarm(shap_values, order = shap_values.abs.max(0), max_display =max_dispaly))
            else:
                st_shap(shap.plots.beeswarm(shap_values, order = shap_values.abs.mean(0), max_display =max_dispaly))

            colored_header(label="SHAP Dependence", description=" ",color_name="violet-30")
            
            # shap.dependence_plot('Si', shap_values, X[cols], interaction_index='Mn', show=False)
            shap_values = explainer.shap_values(fs.features) 
            list_features = fs.features.columns.tolist()
            feature = st.selectbox('feature',list_features)
            interact_feature = st.selectbox('interact feature', list_features)
            st_shap(shap.dependence_plot(feature, shap_values, fs.features, display_features=fs.features,interaction_index=interact_feature))
            
            # colored_header(label="SHAP Most Important Feature", description=" ",color_name="violet-30")
            # shap_values = explainer(fs.features)
            # ind_mean = shap_values.abs.mean(0).argsort[-1]

            # ind_max = shap_values.abs.max(0).argsort[-1]

            # ind_perc = shap_values.abs.percentile(95, 0).argsort[-1]
            # st_shap(shap.plots.scatter(shap_values[:, ind_mean]))           

    
    elif sub_option == "集成学习":
        colored_header(label="集成学习",description=" ",color_name="violet-90")
        sub_sub_option = option_menu(None, ["回归"],
                                icons=['house',  "list-task"],
                                menu_icon="cast", default_index=0, orientation="horizontal")
        
        if sub_sub_option == "回归":
            file = st.file_uploader("Upload `.csv`file", type=['csv'], label_visibility="collapsed")
            if file is None:
                table = PrettyTable(['上传文件名称', '名称','数据说明'])
                table.add_row(['file_1','data set','数据集'])
                st.write(table)
            if file is not None:
                df = pd.read_csv(file)
                # 检测缺失值
                check_string_NaN(df)

                colored_header(label="数据信息", description=" ",color_name="violet-70")
                nrow = st.slider("rows", 1, len(df)-1, 5)
                df_nrow = df.head(nrow)
                st.write(df_nrow)

                colored_header(label="特征变量和目标变量",description=" ",color_name="violet-70")

                target_num = st.number_input('目标变量数量',  min_value=1, max_value=10, value=1)
                
                col_feature, col_target = st.columns(2)
                    
                # features
                features = df.iloc[:,:-target_num]
                # targets
                targets = df.iloc[:,-target_num:]
                with col_feature:    
                    st.write(features.head())
                with col_target:   
                    st.write(targets.head())
            # =================== model ====================================
                reg = REGRESSOR(features,targets)

                colored_header(label="选择目标变量", description=" ", color_name="violet-30")

                target_selected_option = st.selectbox('target', list(reg.targets)[::-1])

                reg.targets = targets[target_selected_option]

                colored_header(label="Regressor", description=" ",color_name="violet-30")

                model_path = './models/el regressors'

                template_alg = model_platform(model_path)

                inputs, col2 = template_alg.show()

                if inputs['model'] == 'BaggingRegressor':
                    with col2:
                        with st.expander('Operator'):
                            preprocess = st.selectbox('data preprocess',['StandardScaler','MinMaxScaler'])

                            operator = st.selectbox('operator', ('train test split','cross val score', 'leave one out'), label_visibility='collapsed')
                            if operator == 'train test split':
                                inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                                if preprocess == 'StandardScaler':
                                    reg.features = StandardScaler().fit_transform(reg.features)
                                if preprocess == 'MinMaxScaler':
                                    reg.features = MinMaxScaler().fit_transform(reg.features)
                                
                                reg.features = pd.DataFrame(reg.features)    
                                
                                reg.Xtrain, reg.Xtest, reg.Ytrain, reg.Ytest = TTS(reg.features,reg.targets,test_size=inputs['test size'],random_state=inputs['random state'])

                            elif operator == 'cross val score':
                                if preprocess == 'StandardScaler':
                                    reg.features = StandardScaler().fit_transform(reg.features)
                                if preprocess == 'MinMaxScaler':
                                    reg.features = MinMaxScaler().fit_transform(reg.features)
                                cv = st.number_input('cv',1,10,5)

                            elif operator == 'leave one out':
                                if preprocess == 'StandardScaler':
                                    reg.features = StandardScaler().fit_transform(reg.features)
                                if preprocess == 'MinMaxScaler':
                                    reg.features = MinMaxScaler().fit_transform(reg.features)
                                reg.features = pd.DataFrame(reg.features)    
                                loo = LeaveOneOut()

                    colored_header(label="Training", description=" ",color_name="violet-30")
                    with st.container():
                        button_train = st.button('Train', use_container_width=True)
                    if button_train:

                        if operator == 'train test split':

                            if inputs['base estimator'] == "DecisionTree": 
                                reg.model = BaggingRegressor(estimator = tree.DecisionTreeRegressor(random_state=inputs['random state']),n_estimators=inputs['nestimators'],
                                                                max_samples=inputs['max samples'], max_features=inputs['max features'], n_jobs=-1) 
                                
                                reg.BaggingRegressor()
                

                                result_data = pd.concat([reg.Ytest, pd.DataFrame(reg.Ypred)], axis=1)
                                result_data.columns = ['actual','prediction']

                                plot_and_export_results(reg, "BaggingR")

                            
                            elif inputs['base estimator'] == "SupportVector": 
                                reg.model = BaggingRegressor(estimator = SVR(),n_estimators=inputs['nestimators'],
                                        max_samples=inputs['max samples'], max_features=inputs['max features'], n_jobs=-1) 
                                reg.BaggingRegressor()

                                result_data = pd.concat([reg.Ytest, pd.DataFrame(reg.Ypred)], axis=1)
                                result_data.columns = ['actual','prediction']

                                plot_and_export_results(reg, "BaggingR")
                            
                            elif inputs['base estimator'] == "LinearRegression": 
                                reg.model = BaggingRegressor(estimator = LinearR(),n_estimators=inputs['nestimators'],
                                        max_samples=inputs['max samples'], max_features=inputs['max features'], n_jobs=-1) 
                                reg.BaggingRegressor()
                

                                result_data = pd.concat([reg.Ytest, pd.DataFrame(reg.Ypred)], axis=1)
                                result_data.columns = ['actual','prediction']

                                plot_and_export_results(reg, "BaggingR")

                        elif operator == 'cross val score':
                            if inputs['base estimator'] == "DecisionTree": 
                                reg.model = BaggingRegressor(estimator = tree.DecisionTreeRegressor(random_state=inputs['random state']),n_estimators=inputs['nestimators'],
                                                                max_samples=inputs['max samples'], max_features=inputs['max features'], n_jobs=-1) 

                                cvs = CV(reg.model, reg.features, reg.targets, cv = cv, scoring=make_scorer(r2_score), return_train_score=False, return_estimator=True)

                                plot_cross_val_results(cvs, "BaggingR_cv")   

                            elif inputs['base estimator'] == "SupportVector": 

                                reg.model = BaggingRegressor(estimator =  SVR(),n_estimators=inputs['nestimators'],
                                        max_samples=inputs['max samples'], max_features=inputs['max features'], n_jobs=-1) 

                                cvs = CV(reg.model, reg.features, reg.targets, cv = cv, scoring=make_scorer(r2_score), return_train_score=False, return_estimator=True)
                    
                                plot_cross_val_results(cvs, "BaggingR_cv")   

                            elif inputs['base estimator'] == "LinearRegression":
                                reg.model = BaggingRegressor(estimator = LinearR(),n_estimators=inputs['nestimators'],
                                        max_samples=inputs['max samples'], max_features=inputs['max features'], n_jobs=-1) 

                                cvs = CV(reg.model, reg.features, reg.targets, cv = cv, scoring=make_scorer(r2_score), return_train_score=False, return_estimator=True)
                    
                                plot_cross_val_results(cvs, "BaggingR_cv")   

                        elif operator == 'leave one out':
                            if inputs['base estimator'] == "DecisionTree": 
                                reg.model = BaggingRegressor(estimator = tree.DecisionTreeRegressor(random_state=inputs['random state']),n_estimators=inputs['nestimators'],
                                        max_samples=inputs['max samples'], max_features=inputs['max features'], n_jobs=-1) 
                            
                                export_loo_results(reg, loo, "BaggingR_loo")

                            elif inputs['base estimator'] == "SupportVector": 

                                reg.model = BaggingRegressor(estimator = SVR(),n_estimators=inputs['nestimators'],
                                        max_samples=inputs['max samples'], max_features=inputs['max features'], n_jobs=-1) 
                                
                                export_loo_results(reg, loo, "BaggingR_loo")

                            elif inputs['base estimator'] == "LinearRegression":
                                reg.model = BaggingRegressor(estimator = LinearR(),n_estimators=inputs['nestimators'],
                                        max_samples=inputs['max samples'], max_features=inputs['max features'], n_jobs=-1) 
                
                                export_loo_results(reg, loo, "BaggingR_loo")

                if inputs['model'] == 'AdaBoostRegressor':

                    with col2:
                        with st.expander('Operator'):
                            operator = st.selectbox('data operator', ('train test split','cross val score','leave one out'))
                        
                            if operator == 'train test split':
                                inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                                reg.Xtrain, reg.Xtest, reg.Ytrain, reg.Ytest = TTS(reg.features,reg.targets,test_size=inputs['test size'],random_state=inputs['random state'])
                            elif operator == 'cross val score':
                                cv = st.number_input('cv',1,10,5)
                            elif operator == 'leave one out':
                                loo = LeaveOneOut()
                    colored_header(label="Training", description=" ",color_name="violet-30")
                    with st.container():
                        button_train = st.button('Train', use_container_width=True)
                    if button_train:

                        if operator == 'train test split':

                            if inputs['base estimator'] == "DecisionTree": 
                                reg.model = AdaBoostRegressor(estimator=tree.DecisionTreeRegressor(), n_estimators=inputs['nestimators'], learning_rate=inputs['learning rate'],random_state=inputs['random state']) 
                                
                                reg.AdaBoostRegressor()
                
                                result_data = pd.concat([reg.Ytest, pd.DataFrame(reg.Ypred)], axis=1)
                                result_data.columns = ['actual','prediction']

                                plot_and_export_results(reg, "AdaBoostR")
                            
                            elif inputs['base estimator'] == "SupportVector": 

                                reg.model = AdaBoostRegressor(estimator=SVR(), n_estimators=inputs['nestimators'], learning_rate=inputs['learning rate'],random_state=inputs['random state'])
                                
                                reg.AdaBoostRegressor()

                                result_data = pd.concat([reg.Ytest, pd.DataFrame(reg.Ypred)], axis=1)
                                result_data.columns = ['actual','prediction']

                                plot_and_export_results(reg, "AdaBoostR")
                            
                            elif inputs['base estimator'] == "LinearRegression": 
                                reg.model = AdaBoostRegressor(estimator=LinearR(), n_estimators=inputs['nestimators'], learning_rate=inputs['learning rate'],random_state=inputs['random state'])
                                reg.AdaBoostRegressor()

                                result_data = pd.concat([reg.Ytest, pd.DataFrame(reg.Ypred)], axis=1)
                                result_data.columns = ['actual','prediction']
                                
                                plot_and_export_results(reg, "AdaBoostR")

                        elif operator == 'cross val score':
                            if inputs['base estimator'] == "DecisionTree": 
                                reg.model =  AdaBoostRegressor(estimator=tree.DecisionTreeRegressor(), n_estimators=inputs['nestimators'], learning_rate=inputs['learning rate'],random_state=inputs['random state']) 
                                cvs = CVS(reg.model, reg.features, reg.targets, cv = cv)
                    
                                st.write('mean cross val R2:', cvs.mean())
                            elif inputs['base estimator'] == "SupportVector": 

                                reg.model =  AdaBoostRegressor(estimator=SVR(), n_estimators=inputs['nestimators'], learning_rate=inputs['learning rate'],random_state=inputs['random state']) 

                                cvs = CV(reg.model, reg.features, reg.targets, cv = cv, scoring=make_scorer(r2_score), return_train_score=False, return_estimator=True)
                    
                                plot_cross_val_results(cvs, "AdaBoostR_cv")  

                            elif inputs['base estimator'] == "LinearRegression":
                                reg.model =  AdaBoostRegressor(estimator=LinearR(), n_estimators=inputs['nestimators'], learning_rate=inputs['learning rate'],random_state=inputs['random state']) 

                                cvs = CV(reg.model, reg.features, reg.targets, cv = cv, scoring=make_scorer(r2_score), return_train_score=False, return_estimator=True)
                    
                                plot_cross_val_results(cvs, "AdaBoostR_cv")  

                        elif operator == 'leave one out':
                            if inputs['base estimator'] == "DecisionTree": 
                                reg.model =  AdaBoostRegressor(estimator=tree.DecisionTreeRegressor(), n_estimators=inputs['nestimators'], learning_rate=inputs['learning rate'],random_state=inputs['random state']) 
                            
                                export_loo_results(reg, loo, "AdaBoostR_loo")
                            
                            elif inputs['base estimator'] == "SupportVector": 

                                reg.model = reg.model = AdaBoostRegressor(estimator=SVR(), n_estimators=inputs['nestimators'], learning_rate=inputs['learning rate'],random_state=inputs['random state']) 
                                
                                export_loo_results(reg, loo, "AdaBoostR_loo")

                            elif inputs['base estimator'] == "LinearRegression":
                                reg.model = reg.model =  AdaBoostRegressor(estimator=LinearR(), n_estimators=inputs['nestimators'], learning_rate=inputs['learning rate'],random_state=inputs['random state']) 
                                                    
                                export_loo_results(reg, loo, "AdaBoostR_loo")
                            
                if inputs['model'] == 'GradientBoostingRegressor':

                    with col2:
                        with st.expander('Operator'):
                            operator = st.selectbox('data operator', ('train test split','cross val score','leave one out'))
                        
                            if operator == 'train test split':
                                inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                                reg.Xtrain, reg.Xtest, reg.Ytrain, reg.Ytest = TTS(reg.features,reg.targets,test_size=inputs['test size'],random_state=inputs['random state'])
                            elif operator == 'cross val score':
                                cv = st.number_input('cv',1,10,5)
                            elif operator == 'leave one out':
                                loo = LeaveOneOut()

                    colored_header(label="Training", description=" ",color_name="violet-30")
                    with st.container():
                        button_train = st.button('Train', use_container_width=True)
                    if button_train:

                        if operator == 'train test split':

                                reg.model = GradientBoostingRegressor(learning_rate=inputs['learning rate'],n_estimators=inputs['nestimators'],max_depth=inputs['max depth'],max_features=inputs['max features'],
                                                                    random_state=inputs['random state']) 
                                
                                reg.AdaBoostRegressor()
                

                                result_data = pd.concat([reg.Ytest, pd.DataFrame(reg.Ypred)], axis=1)
                                result_data.columns = ['actual','prediction']
                                plot_and_export_results(reg, "GradientBoostingR")

                        elif operator == 'cross val score':
                                reg.model = GradientBoostingRegressor(learning_rate=inputs['learning rate'],n_estimators=inputs['nestimators'],max_depth=inputs['max depth'],max_features=inputs['max features'],
                                                                    random_state=inputs['random state'])  
                                cvs = CV(reg.model, reg.features, reg.targets, cv = cv, scoring=make_scorer(r2_score), return_train_score=False, return_estimator=True)
                                plot_cross_val_results(cvs, "GradientBoostingR_cv")    

                        elif operator == 'leave one out':
                                reg.model = GradientBoostingRegressor(learning_rate=inputs['learning rate'],n_estimators=inputs['nestimators'],max_depth=inputs['max depth'],max_features=inputs['max features'],
                                                                    random_state=inputs['random state']) 
                            
                                export_loo_results(reg, loo, "GradientBoostingR_loo")

                if inputs['model'] == 'XGBRegressor':

                    with col2:
                        with st.expander('Operator'):
                            operator = st.selectbox('data operator', ('train test split','cross val score','leave one out'))
                        
                            if operator == 'train test split':
                                inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                                reg.Xtrain, reg.Xtest, reg.Ytrain, reg.Ytest = TTS(reg.features,reg.targets,test_size=inputs['test size'],random_state=inputs['random state'])
                            elif operator == 'cross val score':
                                cv = st.number_input('cv',1,10,5)
                            elif operator == 'leave one out':
                                loo = LeaveOneOut()
                    colored_header(label="Training", description=" ",color_name="violet-30")
                    with st.container():
                        button_train = st.button('Train', use_container_width=True)
                    if button_train:

                        if operator == 'train test split':

                                reg.model = xgb.XGBRegressor(booster=inputs['base estimator'], n_estimators=inputs['nestimators'], 
                                                            max_depth= inputs['max depth'], subsample=inputs['subsample'], colsample_bytree=inputs['subfeature'], 
                                                            learning_rate=inputs['learning rate'])
                                reg.XGBRegressor()

                                result_data = pd.concat([reg.Ytest, pd.DataFrame(reg.Ypred)], axis=1)
                                result_data.columns = ['actual','prediction']

                                plot_and_export_results(reg, "XGBR")

                        elif operator == 'cross val score':
                                reg.model = xgb.XGBRegressor(booster=inputs['base estimator'], n_estimators=inputs['nestimators'], 
                                                            max_depth= inputs['max depth'], subsample=inputs['subsample'], colsample_bytree=inputs['subfeature'], 
                                                            learning_rate=inputs['learning rate'])
                                
                                cvs = CV(reg.model, reg.features, reg.targets, cv = cv, scoring=make_scorer(r2_score), return_train_score=False, return_estimator=True)
                                plot_cross_val_results(cvs, "DTR_cv")    


                        elif operator == 'leave one out':
                                reg.model = xgb.XGBRegressor(booster=inputs['base estimator'], n_estimators=inputs['nestimators'], 
                                                            max_depth= inputs['max depth'], subsample=inputs['subsample'], colsample_bytree=inputs['subfeature'], 
                                                            learning_rate=inputs['learning rate'])
                            
                                export_loo_results(reg, loo, "DTR_loo")


                if inputs['model'] == 'LGBMRegressor':

                    with col2:
                        with st.expander('Operator'):
                            operator = st.selectbox('data operator', ('train test split','cross val score','leave one out'))
                        
                            if operator == 'train test split':
                                inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                                reg.Xtrain, reg.Xtest, reg.Ytrain, reg.Ytest = TTS(reg.features,reg.targets,test_size=inputs['test size'],random_state=inputs['random state'])
                            elif operator == 'cross val score':
                                cv = st.number_input('cv',1,10,5)
                            elif operator == 'leave one out':
                                loo = LeaveOneOut()
                    colored_header(label="Training", description=" ",color_name="violet-30")
                    with st.container():
                        button_train = st.button('Train', use_container_width=True)
                    if button_train:

                        if operator == 'train test split':

                                reg.model = lgb.LGBMRegressor(niterations=inputs['niterations'],nestimators=inputs['nestimators'],learning_rate=inputs['learning rate'],
                                                            num_leaves=inputs['num_leaves'],max_depth=inputs['max depth'])

                                reg.LGBMRegressor()

                                result_data = pd.concat([reg.Ytest, pd.DataFrame(reg.Ypred)], axis=1)
                                result_data.columns = ['actual','prediction']

                                plot_and_export_results(reg, "LGBMR")

                        elif operator == 'cross val score':
                                reg.model = lgb.LGBMRegressor(niterations=inputs['niterations'],nestimators=inputs['nestimators'],learning_rate=inputs['learning rate'],
                                                            num_leaves=inputs['num_leaves'],max_depth=inputs['max depth'])
                                
                                cvs = CV(reg.model, reg.features, reg.targets, cv = cv, scoring=make_scorer(r2_score), return_train_score=False, return_estimator=True)
                                plot_cross_val_results(cvs, "LGBMR_cv")    

                        elif operator == 'leave one out':
                                reg.model = lgb.LGBMRegressor(niterations=inputs['niterations'],nestimators=inputs['nestimators'],learning_rate=inputs['learning rate'],
                                                            num_leaves=inputs['num_leaves'],max_depth=inputs['max depth'])
                                
                                export_loo_results(reg, loo, "LGBMR_loo")

                if inputs['model'] == 'CatBoostRegressor':
                    with col2:
                        with st.expander('Operator'):
                            operator = st.selectbox('data operator', ('train test split','cross val score','leave one out'))
                        
                            if operator == 'train test split':
                                inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                                reg.Xtrain, reg.Xtest, reg.Ytrain, reg.Ytest = TTS(reg.features,reg.targets,test_size=inputs['test size'],random_state=inputs['random state'])
                            elif operator == 'cross val score':
                                cv = st.number_input('cv',1,10,5)
                            elif operator == 'leave one out':
                                loo = LeaveOneOut()
                    colored_header(label="Training", description=" ",color_name="violet-30")
                    with st.container():
                        button_train = st.button('Train', use_container_width=True)
                    if button_train:

                        if operator == 'train test split':

                                reg.model =CatBoostRegressor(iterations=inputs['niteration'],learning_rate=inputs['learning rate'],depth = inputs['max depth'])

                                reg.LGBMRegressor()

                                result_data = pd.concat([reg.Ytest, pd.DataFrame(reg.Ypred)], axis=1)
                                result_data.columns = ['actual','prediction']

                                plot_and_export_results(reg, "CatBoostR")

                        elif operator == 'cross val score':
                                reg.model = CatBoostRegressor(iterations=inputs['niteration'],learning_rate=inputs['learning rate'],depth = inputs['max depth'])
                                
                                cvs = CV(reg.model, reg.features, reg.targets, cv = cv, scoring=make_scorer(r2_score), return_train_score=False, return_estimator=True)
                                plot_cross_val_results(cvs, "CatBoostR_cv")    

                        elif operator == 'leave one out':
                                reg.model = CatBoostRegressor(iterations=inputs['niteration'],learning_rate=inputs['learning rate'],depth = inputs['max depth'])
                                export_loo_results(reg, loo, "CatBoostR_loo")            
                st.write('---')                

        elif sub_sub_option == "分类":
            file = st.file_uploader("Upload `.csv`file", type=['csv'], label_visibility="collapsed")

            if file is not None:
                colored_header(label="Data Information", description=" ", color_name="violet-70")
                with st.expander('Data Information'):
                    df = pd.read_csv(file)
                    check_string_NaN(df)
                    
                    colored_header(label="Data", description=" ",color_name="blue-70")
                    nrow = st.slider("rows", 1, len(df)-1, 5)
                    df_nrow = df.head(nrow)
                    st.write(df_nrow)

                    colored_header(label="Features vs Targets",description=" ",color_name="blue-30")

                    target_num = st.number_input('input target',  min_value=1, max_value=10, value=1)
                    st.write('target number', target_num)
                    
                    col_feature, col_target = st.columns(2)
                    
                    # features
                    features = df.iloc[:,:-target_num]
                    # targets
                    targets = df.iloc[:,-target_num:]
                    with col_feature:    
                        st.write(features.head())
                    with col_target:   
                        st.write(targets.head())
            
                clf = CLASSIFIER(features,targets)

                colored_header(label="Choose Target", description=" ", color_name="violet-30")
                target_selected_option = st.selectbox('target', list(clf.targets)[::-1])

                clf.targets = targets[target_selected_option]

                # st.write(fs.targets.head())
                colored_header(label="Classifier", description=" ",color_name="violet-30")

                model_path = './models/el classifiers'
                
                template_alg = model_platform(model_path)

                colored_header(label="Training", description=" ",color_name="violet-30")

                inputs, col2 = template_alg.show()
            
                if inputs['model'] == 'BaggingClassifier':

                    with col2:
                        with st.expander('Operator'):
                            
                            preprocess = st.selectbox('data preprocess',['StandardScaler','MinMaxScaler'])
                            
                            data_process = st.selectbox('data process', ('train test split','cross val score'))
                            if data_process == 'train test split':
                                inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                                if preprocess == 'StandardScaler':
                                    clf.features = StandardScaler().fit_transform(clf.features)
                                if preprocess == 'MinMaxScaler':
                                    clf.features = MinMaxScaler().fit_transform(clf.features)
                                clf.Xtrain, clf.Xtest, clf.Ytrain, clf.Ytest = TTS(clf.features,clf.targets,test_size=inputs['test size'],random_state=inputs['random state'])
                                
                            elif data_process == 'cross val score':

                                if preprocess == 'StandardScaler':
                                    clf.features = StandardScaler().fit_transform(clf.features)
                                if preprocess == 'MinMaxScaler':
                                    clf.features = MinMaxScaler().fit_transform(clf.features)
                                cv = st.number_input('cv',1,10,5)
                
                    
                    with st.container():
                        button_train = st.button('Train', use_container_width=True)
                    
                    if button_train:
                        if data_process == 'train test split':
                        
                            if inputs['base estimator'] == "DecisionTree":    
                                clf.model = BaggingClassifier(estimator = tree.DecisionTreeClassifier(random_state=inputs['random state']),n_estimators=inputs['nestimators'],
                                                            max_samples=inputs['max samples'], max_features=inputs['max features'], n_jobs=-1) 
        
                                clf.BaggingClassifier()
                                
                                plot = customPlot()
                                cm = confusion_matrix(y_true=clf.Ytest, y_pred=clf.Ypred)
                                plot.confusion_matrix(cm)
                                result_data = pd.concat([clf.Ytest, pd.DataFrame(clf.Ypred)], axis=1)
                                result_data.columns = ['actual','prediction']
                                with st.expander('Actual vs Predict'):
                                    st.write(result_data)
                                    tmp_download_link = download_button(result_data, f'prediction vs actual.csv', button_text='download')
                                    st.markdown(tmp_download_link, unsafe_allow_html=True)
                                                    
                            elif inputs['base estimator'] == "SupportVector": 
                                clf.model = BaggingClassifier(estimator =SVC(), n_estimators=inputs['nestimators'], max_features=inputs['max features'])    

                                clf.BaggingClassifier()
                                
                                plot = customPlot()
                                cm = confusion_matrix(y_true=clf.Ytest, y_pred=clf.Ypred)
                                plot.confusion_matrix(cm)
                                result_data = pd.concat([clf.Ytest, pd.DataFrame(clf.Ypred)], axis=1)
                                result_data.columns = ['actual','prediction']
                                with st.expander('Actual vs Predict'):
                                    st.write(result_data)
                                    tmp_download_link = download_button(result_data, f'prediction vs actual.csv', button_text='download')
                                    st.markdown(tmp_download_link, unsafe_allow_html=True) 
                            
                            elif inputs['base estimator'] == "LogisticRegression":    
                                
                                clf.model = BaggingClassifier(estimator = LR(random_state=inputs['random state']),n_estimators=inputs['nestimators'],
                                                            max_samples=inputs['max samples'], max_features=inputs['max features'], n_jobs=-1)  
                                clf.BaggingClassifier()
                                
                                plot = customPlot()
                                cm = confusion_matrix(y_true=clf.Ytest, y_pred=clf.Ypred)
                                plot.confusion_matrix(cm)
                                result_data = pd.concat([clf.Ytest, pd.DataFrame(clf.Ypred)], axis=1)
                                result_data.columns = ['actual','prediction']
                                with st.expander('Actual vs Predict'):
                                    st.write(result_data)
                                    tmp_download_link = download_button(result_data, f'prediction vs actual.csv', button_text='download')
                                    st.markdown(tmp_download_link, unsafe_allow_html=True) 

                        elif data_process == 'cross val score':

                            if inputs['base estimator'] == "DecisionTree":    
                                clf.model = BaggingClassifier(estimator = tree.DecisionTreeClassifier(random_state=inputs['random state']),n_estimators=inputs['nestimators'],
                                                            max_samples=inputs['max samples'], max_features=inputs['max features'], n_jobs=-1) 
                                cvs = CVS(clf.model, clf.features, clf.targets, cv = cv)

                                st.info('cv mean accuracy score: {}'.format(cvs.mean())) 

                            elif inputs['base estimator'] == "SupportVector": 
                                clf.model = BaggingClassifier(estimator =SVC(), n_estimators=inputs['nestimators'], max_features=inputs['max features'])    
                                cvs = CVS(clf.model, clf.features, clf.targets, cv = cv)

                                st.info('cv mean accuracy score: {}'.format(cvs.mean())) 
                                
                            elif inputs['base estimator'] == "LogisticRegression": 
                                clf.model = BaggingClassifier(estimator = LR(random_state=inputs['random state']),n_estimators=inputs['nestimators'],
                                                            max_samples=inputs['max samples'], max_features=inputs['max features'], n_jobs=-1)                         
                                cvs = CVS(clf.model, clf.features, clf.targets, cv = cv)

                                st.info('cv mean accuracy score: {}'.format(cvs.mean())) 
                
                if inputs['model'] == 'AdaBoostClassifier':

                    with col2:
                        with st.expander('Operator'):
                            
                            preprocess = st.selectbox('data preprocess',['StandardScaler','MinMaxScaler'])
                            
                            data_process = st.selectbox('data process', ('train test split','cross val score'))
                            if data_process == 'train test split':
                                inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                                if preprocess == 'StandardScaler':
                                    clf.features = StandardScaler().fit_transform(clf.features)
                                if preprocess == 'MinMaxScaler':
                                    clf.features = MinMaxScaler().fit_transform(clf.features)
                                clf.Xtrain, clf.Xtest, clf.Ytrain, clf.Ytest = TTS(clf.features,clf.targets,test_size=inputs['test size'],random_state=inputs['random state'])
                                
                            elif data_process == 'cross val score':

                                if preprocess == 'StandardScaler':
                                    clf.features = StandardScaler().fit_transform(clf.features)
                                if preprocess == 'MinMaxScaler':
                                    clf.features = MinMaxScaler().fit_transform(clf.features)
                                cv = st.number_input('cv',1,10,5)
                
                    
                    with st.container():
                        button_train = st.button('Train', use_container_width=True)
                    
                    if button_train:
                        if data_process == 'train test split':
                        
                            if inputs['base estimator'] == "DecisionTree":    
                                clf.model = AdaBoostClassifier(estimator=tree.DecisionTreeClassifier(), n_estimators=inputs['nestimators'], learning_rate=inputs['learning rate'],random_state=inputs['random state'])
        
                                clf.AdaBoostClassifier()
                                
                                plot = customPlot()
                                cm = confusion_matrix(y_true=clf.Ytest, y_pred=clf.Ypred)
                                plot.confusion_matrix(cm)
                                result_data = pd.concat([clf.Ytest, pd.DataFrame(clf.Ypred)], axis=1)
                                result_data.columns = ['actual','prediction']
                                with st.expander('Actual vs Predict'):
                                    st.write(result_data)
                                    tmp_download_link = download_button(result_data, f'prediction vs actual.csv', button_text='download')
                                    st.markdown(tmp_download_link, unsafe_allow_html=True)
                                                    
                            elif inputs['base estimator'] == "SupportVector": 
                                
                                clf.model = AdaBoostClassifier(estimator=SVC(),algorithm='SAMME', n_estimators=inputs['nestimators'], learning_rate=inputs['learning rate'],random_state=inputs['random state'])
        
                                clf.AdaBoostClassifier()
                                
                                plot = customPlot()
                                cm = confusion_matrix(y_true=clf.Ytest, y_pred=clf.Ypred)
                                plot.confusion_matrix(cm)
                                result_data = pd.concat([clf.Ytest, pd.DataFrame(clf.Ypred)], axis=1)
                                result_data.columns = ['actual','prediction']
                                with st.expander('Actual vs Predict'):
                                    st.write(result_data)
                                    tmp_download_link = download_button(result_data, f'prediction vs actual.csv', button_text='download')
                                    st.markdown(tmp_download_link, unsafe_allow_html=True) 
                            
                            elif inputs['base estimator'] == "LogisticRegression":    
                                
                                clf.model = AdaBoostClassifier(estimator=LR(), n_estimators=inputs['nestimators'], learning_rate=inputs['learning rate'],random_state=inputs['random state'])
        
                                clf.AdaBoostClassifier()
                                
                                plot = customPlot()
                                cm = confusion_matrix(y_true=clf.Ytest, y_pred=clf.Ypred)
                                plot.confusion_matrix(cm)
                                result_data = pd.concat([clf.Ytest, pd.DataFrame(clf.Ypred)], axis=1)
                                result_data.columns = ['actual','prediction']
                                with st.expander('Actual vs Predict'):
                                    st.write(result_data)
                                    tmp_download_link = download_button(result_data, f'prediction vs actual.csv', button_text='download')
                                    st.markdown(tmp_download_link, unsafe_allow_html=True) 

                        elif data_process == 'cross val score':

                            if inputs['base estimator'] == "DecisionTree":    
                                clf.model = BaggingClassifier(estimator = tree.DecisionTreeClassifier(random_state=inputs['random state']),n_estimators=inputs['nestimators'],
                                                            max_samples=inputs['max samples'], max_features=inputs['max features'], n_jobs=-1) 
                                cvs = CVS(clf.model, clf.features, clf.targets, cv = cv)

                                st.info('cv mean accuracy score: {}'.format(cvs.mean())) 

                            elif inputs['base estimator'] == "SupportVector": 
                                clf.model = BaggingClassifier(estimator =SVC(), n_estimators=inputs['nestimators'], max_features=inputs['max features'])    
                                cvs = CVS(clf.model, clf.features, clf.targets, cv = cv)

                                st.info('cv mean accuracy score: {}'.format(cvs.mean())) 
                                
                            elif inputs['base estimator'] == "LogisticRegression": 
                                clf.model = BaggingClassifier(estimator = LR(random_state=inputs['random state']),n_estimators=inputs['nestimators'],
                                                            max_samples=inputs['max samples'], max_features=inputs['max features'], n_jobs=-1)                         
                                cvs = CVS(clf.model, clf.features, clf.targets, cv = cv)

                                st.info('cv mean accuracy score: {}'.format(cvs.mean())) 
                
                if inputs['model'] == 'GradientBoostingClassifier':

                    with col2:
                        with st.expander('Operator'):
                            
                            preprocess = st.selectbox('data preprocess',['StandardScaler','MinMaxScaler'])
                            
                            data_process = st.selectbox('data process', ('train test split','cross val score'))
                            if data_process == 'train test split':
                                inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                                if preprocess == 'StandardScaler':
                                    clf.features = StandardScaler().fit_transform(clf.features)
                                if preprocess == 'MinMaxScaler':
                                    clf.features = MinMaxScaler().fit_transform(clf.features)
                                clf.Xtrain, clf.Xtest, clf.Ytrain, clf.Ytest = TTS(clf.features,clf.targets,test_size=inputs['test size'],random_state=inputs['random state'])
                                
                            elif data_process == 'cross val score':

                                if preprocess == 'StandardScaler':
                                    clf.features = StandardScaler().fit_transform(clf.features)
                                if preprocess == 'MinMaxScaler':
                                    clf.features = MinMaxScaler().fit_transform(clf.features)
                                cv = st.number_input('cv',1,10,5)
                
                    
                    with st.container():
                        button_train = st.button('Train', use_container_width=True)
                    
                    if button_train:
                        if data_process == 'train test split':
                        
                                clf.model = GradientBoostingClassifier(learning_rate=inputs['learning rate'],n_estimators=inputs['nestimators'],max_depth=inputs['max depth'],max_features=inputs['max features'],
                                                                    random_state=inputs['random state'])
                                clf.GradientBoostingClassifier()
                                
                                plot = customPlot()
                                cm = confusion_matrix(y_true=clf.Ytest, y_pred=clf.Ypred)
                                plot.confusion_matrix(cm)
                                result_data = pd.concat([clf.Ytest, pd.DataFrame(clf.Ypred)], axis=1)
                                result_data.columns = ['actual','prediction']
                                with st.expander('Actual vs Predict'):
                                    st.write(result_data)
                                    tmp_download_link = download_button(result_data, f'prediction vs actual.csv', button_text='download')
                                    st.markdown(tmp_download_link, unsafe_allow_html=True)

                        elif data_process == 'cross val score':
                                
                                clf.model = GradientBoostingClassifier(learning_rate=inputs['learning rate'],n_estimators=inputs['nestimators'],max_depth=inputs['max depth'],max_features=inputs['max features'],
                                                                    random_state=inputs['random state'])
        
                                cvs = CVS(clf.model, clf.features, clf.targets, cv = cv)

                                st.info('cv mean accuracy score: {}'.format(cvs.mean())) 

                if inputs['model'] == 'XGBClassifier':

                    with col2:
                        with st.expander('Operator'):
                            
                            preprocess = st.selectbox('data preprocess',['StandardScaler','MinMaxScaler'])
                            
                            data_process = st.selectbox('data process', ('train test split','cross val score'))
                            if data_process == 'train test split':
                                inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                                if preprocess == 'StandardScaler':
                                    clf.features = StandardScaler().fit_transform(clf.features)
                                if preprocess == 'MinMaxScaler':
                                    clf.features = MinMaxScaler().fit_transform(clf.features)
                                clf.Xtrain, clf.Xtest, clf.Ytrain, clf.Ytest = TTS(clf.features,clf.targets,test_size=inputs['test size'],random_state=inputs['random state'])
                                
                            elif data_process == 'cross val score':

                                if preprocess == 'StandardScaler':
                                    clf.features = StandardScaler().fit_transform(clf.features)
                                if preprocess == 'MinMaxScaler':
                                    clf.features = MinMaxScaler().fit_transform(clf.features)
                                cv = st.number_input('cv',1,10,5)
                
                    
                    with st.container():
                        button_train = st.button('Train', use_container_width=True)
                    
                    if button_train:
                        if data_process == 'train test split':
                        
                                clf.model = xgb.XGBClassifier(booster=inputs['base estimator'], n_estimators=inputs['nestimators'], 
                                                            max_depth= inputs['max depth'], subsample=inputs['subsample'], colsample_bytree=inputs['subfeature'], 
                                                            learning_rate=inputs['learning rate'])
                                clf.XGBClassifier()
                                
                                plot = customPlot()
                                cm = confusion_matrix(y_true=clf.Ytest, y_pred=clf.Ypred)
                                plot.confusion_matrix(cm)
                                result_data = pd.concat([clf.Ytest, pd.DataFrame(clf.Ypred)], axis=1)
                                result_data.columns = ['actual','prediction']
                                with st.expander('Actual vs Predict'):
                                    st.write(result_data)
                                    tmp_download_link = download_button(result_data, f'prediction vs actual.csv', button_text='download')
                                    st.markdown(tmp_download_link, unsafe_allow_html=True)

                        elif data_process == 'cross val score':
                                
                                clf.model = xgb.XGBClassifier(booster=inputs['base estimator'], n_estimators=inputs['nestimators'], 
                                                            max_depth= inputs['max depth'], subsample=inputs['subsample'], colsample_bytree=inputs['subfeature'], 
                                                            learning_rate=inputs['learning rate'])
        
                                cvs = CVS(clf.model, clf.features, clf.targets, cv = cv)

                                st.info('cv mean accuracy score: {}'.format(cvs.mean())) 
                
                if inputs['model'] == 'LGBMClassifier':

                    with col2:
                        with st.expander('Operator'):
                            
                            preprocess = st.selectbox('data preprocess',['StandardScaler','MinMaxScaler'])
                            
                            data_process = st.selectbox('data process', ('train test split','cross val score'))
                            if data_process == 'train test split':
                                inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                                if preprocess == 'StandardScaler':
                                    clf.features = StandardScaler().fit_transform(clf.features)
                                if preprocess == 'MinMaxScaler':
                                    clf.features = MinMaxScaler().fit_transform(clf.features)
                                clf.Xtrain, clf.Xtest, clf.Ytrain, clf.Ytest = TTS(clf.features,clf.targets,test_size=inputs['test size'],random_state=inputs['random state'])
                                
                            elif data_process == 'cross val score':

                                if preprocess == 'StandardScaler':
                                    clf.features = StandardScaler().fit_transform(clf.features)
                                if preprocess == 'MinMaxScaler':
                                    clf.features = MinMaxScaler().fit_transform(clf.features)
                                cv = st.number_input('cv',1,10,5)
                
                    
                    with st.container():
                        button_train = st.button('Train', use_container_width=True)
                    
                    if button_train:
                        if data_process == 'train test split':
                        
                            clf.model = lgb.LGBMClassifier(niterations=inputs['niterations'],nestimators=inputs['nestimators'],learning_rate=inputs['learning rate'],
                                                            num_leaves=inputs['num_leaves'],max_depth=inputs['max depth'])

                            clf.LGBMClassifier()
                            
                            plot = customPlot()
                            cm = confusion_matrix(y_true=clf.Ytest, y_pred=clf.Ypred)
                            plot.confusion_matrix(cm)
                            result_data = pd.concat([clf.Ytest, pd.DataFrame(clf.Ypred)], axis=1)
                            result_data.columns = ['actual','prediction']
                            with st.expander('Actual vs Predict'):
                                st.write(result_data)
                                tmp_download_link = download_button(result_data, f'prediction vs actual.csv', button_text='download')
                                st.markdown(tmp_download_link, unsafe_allow_html=True)

                        elif data_process == 'cross val score':
                                
                            clf.model = lgb.LGBMClassifier(niterations=inputs['niterations'],nestimators=inputs['nestimators'],learning_rate=inputs['learning rate'],
                                                            num_leaves=inputs['num_leaves'],max_depth=inputs['max depth'])

                            cvs = CVS(clf.model, clf.features, clf.targets, cv = cv)

                            st.info('cv mean accuracy score: {}'.format(cvs.mean()))        

                if inputs['model'] == 'CatBoostClassifier':

                    with col2:
                        with st.expander('Operator'):
                            
                            preprocess = st.selectbox('data preprocess',['StandardScaler','MinMaxScaler'])
                            
                            data_process = st.selectbox('data process', ('train test split','cross val score'))
                            if data_process == 'train test split':
                                inputs['test size'] = st.slider('test size',0.1, 0.5, 0.2)  
                                if preprocess == 'StandardScaler':
                                    clf.features = StandardScaler().fit_transform(clf.features)
                                if preprocess == 'MinMaxScaler':
                                    clf.features = MinMaxScaler().fit_transform(clf.features)
                                clf.Xtrain, clf.Xtest, clf.Ytrain, clf.Ytest = TTS(clf.features,clf.targets,test_size=inputs['test size'],random_state=inputs['random state'])
                                
                            elif data_process == 'cross val score':

                                if preprocess == 'StandardScaler':
                                    clf.features = StandardScaler().fit_transform(clf.features)
                                if preprocess == 'MinMaxScaler':
                                    clf.features = MinMaxScaler().fit_transform(clf.features)
                                cv = st.number_input('cv',1,10,5)
                
                    
                    with st.container():
                        button_train = st.button('Train', use_container_width=True)
                    
                    if button_train:
                        if data_process == 'train test split':
                        
                                clf.model = CatBoostClassifier(iterations=inputs['niteration'],learning_rate=inputs['learning rate'],depth = inputs['max depth'])

                                clf.CatBoostClassifier()
                                
                                plot = customPlot()
                                cm = confusion_matrix(y_true=clf.Ytest, y_pred=clf.Ypred)
                                plot.confusion_matrix(cm)
                                result_data = pd.concat([clf.Ytest, pd.DataFrame(clf.Ypred)], axis=1)
                                result_data.columns = ['actual','prediction']
                                with st.expander('Actual vs Predict'):
                                    st.write(result_data)
                                    tmp_download_link = download_button(result_data, f'prediction vs actual.csv', button_text='download')
                                    st.markdown(tmp_download_link, unsafe_allow_html=True)

                        elif data_process == 'cross val score':
                                
                                clf.model = CatBoostClassifier(iterations=inputs['niteration'],learning_rate=inputs['learning rate'],depth = inputs['max depth'])
        
                                cvs = CVS(clf.model, clf.features, clf.targets, cv = cv)

                                st.info('cv mean accuracy score: {}'.format(cvs.mean()))                 
    
    elif sub_option == "模型推理":
        
        colored_header(label="模型推理",description=" ",color_name="violet-90")
        file = st.file_uploader("Upload `.csv`file", type=['csv'], label_visibility="collapsed", accept_multiple_files=True)
        if len(file) < 2:
            table = PrettyTable(['上传文件名称', '名称','数据说明'])
            table.add_row(['file_1','data set','数据集'])
            table.add_row(['file_2','model','模型'])
            st.write(table)
        elif len(file) == 2:
            df = pd.read_csv(file[0])
            model_file = file[1]
            # 检测缺失值
            check_string_NaN(df)

            colored_header(label="数据信息", description=" ",color_name="violet-70")
            nrow = st.slider("rows", 1, len(df)-1, 5)
            df_nrow = df.head(nrow)
            st.write(df_nrow)

            colored_header(label="特征变量和目标变量",description=" ",color_name="violet-70")

            target_num = st.number_input('目标变量数量',  min_value=1, max_value=10, value=1)

            col_feature, col_target = st.columns(2)
            # features
            features = df.iloc[:,:-target_num]
            # targets
            targets = df.iloc[:,-target_num:]
            with col_feature:    
                st.write(features.head())
            with col_target:   
                st.write(targets.head())    
            colored_header(label="选择目标变量", description=" ", color_name="violet-70")

            target_selected_option = st.selectbox('target', list(targets)[::-1])

            targets = targets[target_selected_option]
            preprocess = st.selectbox('data preprocess',[None, 'StandardScaler','MinMaxScaler'])
            if preprocess == 'StandardScaler':
                features = StandardScaler().fit_transform(features)
            elif preprocess == 'MinMaxScaler':
                features = MinMaxScaler().fit_transform(features)

            # model_file = st.file_uploader("Upload `.pickle`model",  label_visibility="collapsed")
            # if model_file is not None:
            model = pickle.load(model_file)
            prediction = model.predict(features)

            plot = customPlot()
            plot.pred_vs_actual(targets, prediction)
            r2 = r2_score(targets, prediction)
            st.write('R2: {}'.format(r2))
            result_data = pd.concat([targets, pd.DataFrame(prediction)], axis=1)
            result_data.columns = ['actual','prediction']
            with st.expander('预测结果'):
                st.write(result_data)
                tmp_download_link = download_button(result_data, f'预测结果.csv', button_text='download')
                st.markdown(tmp_download_link, unsafe_allow_html=True)
            st.write('---')

    elif sub_option == "符号回归":
        st.write("sisso")
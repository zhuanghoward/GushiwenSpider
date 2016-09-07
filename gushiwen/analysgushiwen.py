# _*_ coding:utf8 _*_

# 作者: W.S.K
"""
遍历指定目录下的所有文件，根据获取到的文件名判断是否为目录，递归判断
根据目录结构创建字典文件，字典文件保存到本地
字典结构见val = dict()
"""
import re
import os
import pickle

class AnalysGushiwen():

    def __init__(self, basepath):
        self.keyslist = [u'先秦', u'两汉', u'魏晋', u'南北朝', u'隋代', u'唐代',
                         u'五代', u'宋代', u'金朝', u'元代', u'明代', u'清代', ]
        self.val = dict(
            #  统计所有文本部分，用于词频分析
            content_poetry_merge='',  # 所有作品正文累加
            content_fanyi_merge='',  # 所有作品翻译、赏析累加
            content_author_intro_merge='',  # 所有作者介绍累加
            content_poetry_single=dict(
                # 统计该作者名下所有作品原文
                # author1 = 'author1',
            ),
            content_fanyi_single=dict(
                # 统计该作者名下所有作品翻译、赏析
                #  author1= 'author1',
            ),
            content_author_intro_single=dict(
                # 统计该作者的介绍
            ),

            # 统计所有数据部分，用于数据分析
            account_poetry=dict(
                author_all=0,  # 所有作者总数
                author_list=[],
                poetry_all=0,  # 所有作品个数
                poetry_list=[],
                author_single=dict(
                    # 统计每个作者的作品数量
                    # author2=20,
                ),
            ),

            # 统计所有评分数据部分
            account_score=dict(
                score_max=10,  # 分数排名通过内置函数（如sort）或者pandas处理
                score_min=0,
                score_populate=0,  # 打分总人数
                score_total=0,
                score_average=0,
                score_single_author=dict(
                    # author_name = {
                    #     score_max = 0,
                    #     score_min = 0,
                    #     score_populate = 0,  #打分总人数
                    #     score_total = 0，
                    #     score_average = 0,
                    #     poetryname={score=float(score), score_populate=score_populate},
                    # },
                ),
            ),
        )

        # 初始化所有的字典，朝代为键值
        self.dic_dystany = {k: self.val for k in self.keyslist}
        self.basepath = base_path


    def extractdata(self):
        base_dir = u'dir'
        for dystany in self.keyslist:
        # for dystany in [u'金朝', u'先秦']:  #以金朝为测试目标
            # 各朝代内容（正文、翻译、作者介绍）汇总
            con_pty_mrg = self.dic_dystany[dystany]['content_poetry_merge']
            con_fy_mrg = self.dic_dystany[dystany]['content_fanyi_merge']
            con_ath_intr_mrg = self.dic_dystany[dystany]['content_author_intro_merge']
            author_list = os.listdir(os.path.join(base_dir, dystany))  # [u'元好问', u'刘迎', u'赵秉文']
            self.dic_dystany[dystany]['account_poetry']['author_all'] = len(author_list)
            self.dic_dystany[dystany]['account_poetry']['author_list'] = author_list
            self.dic_dystany[dystany]['account_poetry']['poetry_list'] = []
            dystany_poetry_list = self.dic_dystany[dystany]['account_poetry']['poetry_list']
            for author in author_list:
                # 各作者内容（正文、翻译、作者介绍）汇总
                self.dic_dystany[dystany]['content_poetry_single'][author] = ''
                con_pty_sgl = self.dic_dystany[dystany]['content_poetry_single'][author]
                self.dic_dystany[dystany]['content_fanyi_single'][author] = ''
                con_fy_sgl = self.dic_dystany[dystany]['content_fanyi_single'][author]

                # 单个作者作品数量统计
                self.dic_dystany[dystany]['account_poetry']['author_single'][author] = 0
                acnt_pty_ath_sgl = self.dic_dystany[dystany]['account_poetry']['author_single'][author]

                # 评分内容统计：  作者评分汇总 ， 作品评分汇总
                self.dic_dystany[dystany]['account_score']['score_single_author'][author] = {}
                scr_sgl_ath = self.dic_dystany[dystany]['account_score']['score_single_author'][author]
                scr_sgl_ath['score_max'] = 10.0
                scr_sgl_ath['score_min'] = 0.0
                scr_sgl_ath['score_populate'] = 0  #  总评分人数
                scr_sgl_ath['score_total'] = 0           # 各作品评分累加
                scr_sgl_ath['score_average'] = 0         # 总分除以作品数

                # 获取作者目录下的所有文件，识别作者介绍与作品
                cur_path = os.path.join(base_dir, dystany, author)
                txt_list = os.listdir(cur_path)
                ath_intr_file_name_list = [fn for fn in txt_list if u'简介' in fn]
                # 判断有无作者，有作者的才会统计作者相关
                if ath_intr_file_name_list:
                    ath_intr_file_name = ath_intr_file_name_list[0]
                    ath_intr_file = open(os.path.join(cur_path, ath_intr_file_name), 'r')
                    ath_intr = ath_intr_file.read().decode('utf8')
                    ath_intr_file.close()

                    # 处理作者介绍部分
                    con_ath_intr_mrg = con_ath_intr_mrg + ath_intr  # 计入所有作者简介总和
                    # 单个作者介绍不需要累加记录
                    self.dic_dystany[dystany]['content_author_intro_single'][author] = ath_intr

                    # 处理作品部分,当前作者名下的所有作品列表
                    txt_list.remove(ath_intr_file_name)  # 返回值为None，不能直接赋值给新列表
                    acnt_pty_ath_sgl = len(txt_list)
                    dystany_poetry_list = dystany_poetry_list + txt_list
                    for ptr in txt_list:
                        ptr_file = open(os.path.join(cur_path, ptr), 'r')
                        ptr_con = ptr_file.read().decode('utf8')
                        ptr_file.close()
                        title, score, score_populate, yuanwen, yuanwen_link, fanyi = self.extract_content(ptr_con)
                        # 正文汇总、翻译汇总
                        con_pty_mrg = con_pty_mrg + yuanwen
                        con_fy_mrg = con_fy_mrg + fanyi
                        # 各作者所有文章的正文、翻译汇总
                        con_pty_sgl = con_pty_sgl + yuanwen
                        con_fy_sgl = con_fy_sgl + fanyi
                        # 各作者名下单作品评分
                        poetry_name = ptr.replace(u'.txt', '')
                        scr_sgl_ath[poetry_name] = dict(score=float(score), score_populate=int(score_populate))
                else:
                    # 佚名或者类似于孟子及其弟子或者刘向 撰暂且忽略不计，只有先秦和两汉有一小部分
                    con_ath_inr_sgl = u'NoAuthor'
                    # 无作者简介，全部都是作品了
                    acnt_pty_ath_sgl = len(txt_list)
                    dystany_poetry_list = dystany_poetry_list + txt_list
                    for ptr in txt_list:
                        ptr_file = open(os.path.join(cur_path, ptr), 'r')
                        ptr_con = ptr_file.read().decode('utf8')
                        ptr_file.close()
                        title, score, score_populate, yuanwen, yuanwen_link, fanyi = self.extract_content(ptr_con)
                        # 正文汇总、翻译汇总
                        con_pty_mrg = con_pty_mrg + yuanwen
                        con_fy_mrg = con_fy_mrg + fanyi
                        # 各作者所有文章的正文、翻译汇总
                        con_pty_sgl = con_pty_sgl + yuanwen
                        con_fy_sgl = con_fy_sgl + fanyi
                        # 各作者名下单作品评分
                        poetry_name = ptr.replace(u'.txt', '')
                        scr_sgl_ath[poetry_name] = dict(score=float(score), score_populate=int(score_populate))

    @staticmethod
    def extract_content(content):
        """
        内容处理注意事项
        1、 剔除的文本内容
        2、正文部分提取， 需考虑译文是否存在。评分是否存在
        """
        rm_con1 = u'本页内容整理自网络（或由匿名网友上传），原作者已无法考证，版权归原作者所有。'
        rm_con2 = u'本站免费发布仅供学习参考，其观点不代表本站立场。站务邮箱：service@gushiwen.org'
        rm_con3 = u'作者：佚名'  # 翻译和赏析的作者基本都是佚名
        content = content.replace(rm_con1, '').replace(rm_con2, '').replace(rm_con3, '')

        if u'译文及注释' in content:
            if u'评分人数不足' in content:
                # 记为0分
                pattern = u'(.*?)原文链接：(.*?)\(评分人数不足\)(.*?)原文：(.*?)译文及注释(.*)'
                match = re.findall(pattern, content, re.S)
                try:
                    title = match[0][0]
                except IndexError:
                    # 存在一些脏数据，在翻译后面缀上不完整的原文和评分人数不足，由于太少，手工清理。
                    print content[:100]
                yuanwen_link = match[0][1]
                score_populate = 0
                score = 0
                yuanwen = match[0][3]   # 2 是作者，忽略
                fanyi = match[0][4]
            else:
                pattern = u'(.*?)原文链接：(.*?)\((.*?)人评分\)(.*?)朝代(.*?)原文：(.*?)译文及注释(.*)'
                match = re.findall(pattern, content, re.S)
                title = match[0][0]
                yuanwen_link = match[0][1]
                score_populate = match[0][2]
                score = match[0][3]
                yuanwen = match[0][5]  # 4 是作者，忽略
                fanyi = match[0][6]
        elif u'译文' in content:
            if u'评分人数不足' in content:
                pattern = u'(.*?)原文链接：(.*?)\(评分人数不足\)(.*?)原文：(.*?)译文(.*)'
                match = re.findall(pattern, content, re.S)
                title = match[0][0]
                yuanwen_link = match[0][1]
                score_populate = 0
                score = 0
                yuanwen = match[0][3]  # 2 是作者，忽略
                fanyi = match[0][4]
            else:
                pattern = u'(.*?)原文链接：(.*?)\((.*?)人评分\)(.*?)朝代(.*?)原文：(.*?)译文(.*)'
                match = re.findall(pattern, content, re.S)
                title = match[0][0]
                yuanwen_link = match[0][1]
                score_populate = match[0][2]
                score = match[0][3]
                yuanwen = match[0][5]  # 4 是作者，忽略
                fanyi = match[0][6]
        else:
            # 没有译文的文章，部分会有赏析部分，但数量极少。整个文本内容既作为正文又作为翻译部分处理
            title = ''
            score = 0
            score_populate = 0
            yuanwen = content
            yuanwen_link = '',
            fanyi = content  # 翻译为空

        return title, score, score_populate, yuanwen, yuanwen_link, fanyi


if __name__ == '__main__':
    base_path = u'dir'
    Analys = AnalysGushiwen(base_path)
    Analys.extractdata()
    stop_words = [u'译文', u'注释', u'赏析', u'创作背景', u'参考资料']
    analysedic = open('analyse.pkl', 'wb')
    pickle.dump(Analys.dic_dystany, analysedic)
    analysedic.close()

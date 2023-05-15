import json
import os
import re
import warnings


class utils:
    @staticmethod
    def replace_func(m, params):
        return (
            str(round(float(params[int(m.group(1)) - 1]) * 100)) + "%"
            if m.group(2) == "%"
            else str(round(params[int(m.group(1)) - 1]))
        )

    # 替换含参数的字段，删除html标签
    @staticmethod
    def processDesc(desc, params):
        if (
            isinstance(params, list)
            and len(params) > 0
            and isinstance(params[0], dict)
            and "Value" in params[0]
        ):
            params = [param["Value"] for param in params]
        pDesc = desc
        # 替换参数
        pDesc = re.sub(
            r"#(\d+)\[i\](%?)",
            lambda m: utils.replace_func(m, params),
            pDesc,
        )
        # 删除html标签
        pDesc = re.sub(r"<[^>]+>", "", pDesc)
        return pDesc

    # 获取静态Hash
    @staticmethod
    def get_stable_hash(string: str) -> int:
        hash1 = 5381
        hash2 = hash1

        for i in range(0, len(string), 2):
            hash1 = ((hash1 << 5) + hash1) & 0xFFFFFFFF ^ ord(string[i])
            if i == len(string) - 1:
                break
            hash2 = ((hash2 << 5) + hash2) & 0xFFFFFFFF ^ ord(string[i + 1])

        result = (hash1 + (hash2 * 1566083941)) & 0xFFFFFFFF
        return result if result <= 0x7FFFFFFF else result - 0x100000000

    # 替换所有的Value字典为对应的数值
    @staticmethod
    def replaceValueDict(valueDict):
        if isinstance(valueDict, dict):
            if "Value" in valueDict:
                return valueDict["Value"]
            else:
                return {k: utils.replaceValueDict(v) for k, v in valueDict.items()}
        elif isinstance(valueDict, list):
            return [utils.replaceValueDict(v) for v in valueDict]
        else:
            return valueDict


class StarRailData:
    def __init__(self, language="CN"):
        self.language = language

    def load_data(self, path_to_starraildata, path_to_data):
        pathDataBase = path_to_starraildata
        pathData = path_to_data
        pathExcelOutput = os.path.join(pathDataBase, "ExcelOutput")
        pathTextMap = os.path.join(pathDataBase, "TextMap")
        pathAvatarConfig = os.path.join(pathExcelOutput, "AvatarConfig.json")
        pathAvatarPromotionConfig = os.path.join(
            pathExcelOutput, "AvatarPromotionConfig.json"
        )
        pathAvatarSkillConfig = os.path.join(pathExcelOutput, "AvatarSkillConfig.json")
        pathAvatarSkillTreeConfig = os.path.join(
            pathExcelOutput, "AvatarSkillTreeConfig.json"
        )
        pathSkillTreeConfig = os.path.join(pathData, "SkillTree.json")
        pathAvatarRankConfig = os.path.join(pathExcelOutput, "AvatarRankConfig.json")
        pathExtraEffectConfig = os.path.join(pathExcelOutput, "ExtraEffectConfig.json")
        pathTextMap = os.path.join(pathTextMap, "TextMap" + self.language + ".json")

        # read all json
        with open(pathAvatarConfig, "r", encoding="utf-8") as f:
            self.avatarConfig = json.load(f)
        with open(pathAvatarPromotionConfig, "r", encoding="utf-8") as f:
            self.avatarPromotionConfig = json.load(f)
        with open(pathAvatarSkillConfig, "r", encoding="utf-8") as f:
            self.avatarSkillConfig = json.load(f)
        with open(pathAvatarSkillTreeConfig, "r", encoding="utf-8") as f:
            self.avatarSkillTreeConfig = json.load(f)
        with open(pathSkillTreeConfig, "r", encoding="utf-8") as f:
            self.skillTreeConfig = json.load(f)
        with open(pathAvatarRankConfig, "r", encoding="utf-8") as f:
            self.avatarRankConfig = json.load(f)
        with open(pathExtraEffectConfig, "r", encoding="utf-8") as f:
            self.extraEffectConfig = json.load(f)
        with open(pathTextMap, "r", encoding="utf-8") as f:
            self.textMap = json.load(f)

    # 读取技能列表
    def getAvatarSkillList(
        self, avatarNameOrKey, levels=[6, 10, 10, 10], selectKeys=None
    ):
        # 参数检查
        if isinstance(avatarNameOrKey, int):
            avatarKey = str(avatarNameOrKey)  # 转换为字符串
        if isinstance(avatarNameOrKey, str):
            avatarKey = next(
                (
                    k
                    for k, v in self.avatarConfig.items()
                    if str(v["AvatarName"]["Hash"]) in self.textMap
                    and self.textMap[str(v["AvatarName"]["Hash"])] == avatarNameOrKey
                ),
                None,
            )
        if not isinstance(levels, list):
            warnings.warn("level must be a list, using default value [6,10,10,10]")
            levels = [6, 10, 10, 10]  # 不是列表类型，使用默认值
        elif len(levels) != 4:
            warnings.warn(
                "level must contain exactly 4 integers, using default value [6,10,10,10]"
            )
            levels = [6, 10, 10, 10]  # 不是长度为4的列表，使用默认值
        elif not all(
            1 <= levels[i] <= limits[i] for i, limits in enumerate([(9,), (15, 15, 15)])
        ):
            warnings.warn("Invalid value for level, using default value [6,10,10,10]")
            levels = [6, 10, 10, 10]  # 值不在范围内，使用默认值
        if selectKeys is None:
            # selectKeys = {"SkillID", "SkillName", "SkillTag", "SkillTypeDesc", "Level", "MaxLevel", "SkillDesc", "SimpleSkillDesc", "RatedSkillTreeID",\
            #       "RatedRankID", "ExtraEffectIDList", "SimpleExtraEffectIDList", "SPBase", "ParamList", "SimpleParamList", "StanceDamageType",\
            #       "AttackType", "SkillEffect", "SkillComboValueDelta"}
            # selectKeys = {"SkillName", "SkillTag", "SkillTypeDesc", "Level", "MaxLevel", "SkillDesc", "SPBase"}
            selectKeys = {
                "SkillName",
                "SkillTag",
                "SkillTypeDesc",
                "SkillDesc",
                "SPBase",
            }
        # 读取角色技能列表
        skillList = []
        levelDict = {
            "Normal": levels[0],
            "BPSkill": levels[1],
            "Ultra": levels[2],
            "Maze": 1,
        }
        for skillID in self.avatarConfig[avatarKey]["SkillList"]:
            rawSkillConfig = self.avatarSkillConfig[str(skillID)]  # 读取技能配置
            attack_type = rawSkillConfig.get("1", {}).get("AttackType")  # 读取技能等级
            if attack_type == "MazeNormal":
                continue  # 不读取箱庭普攻
            level = levelDict.get(attack_type, levels[3])  # 读取对应等级
            rawSkillConfig = rawSkillConfig[str(level)]  # 选取需要的字段
            skillConfig = {
                k: rawSkillConfig[k]
                for k in selectKeys.intersection(rawSkillConfig.keys())
            }
            skillConfig = {
                k: skillConfig[k] for k in selectKeys if k in skillConfig.keys()
            }
            # 处理字段
            for key, value in skillConfig.items():
                if isinstance(value, dict) and "Hash" in value:
                    if str(value["Hash"]) in self.textMap:
                        skillConfig[key] = self.textMap[str(value["Hash"])]
                        if key == "SkillDesc" or key == "SimpleSkillDesc":
                            skillConfig[key] = utils.processDesc(
                                skillConfig[key], rawSkillConfig["ParamList"]
                            )
                    else:  # 替换为空值
                        skillConfig[key] = ""
            skillConfig = utils.replaceValueDict(skillConfig)
            skillConfig = {k: v for k, v in skillConfig.items() if v != ""}  # 删除空值
            skillList.append(skillConfig)

        return skillList

    # 读取角色名列表
    def getAvatarNameList(self):
        return {
            k: self.textMap[str(self.avatarConfig[k]["AvatarName"]["Hash"])]
            for k in self.avatarConfig.keys()
        }

    # 读取角色星魂(Rank)列表
    def getAvatarRankList(self, avatarNameOrKey, selectKeys=None):
        # 参数检查
        if isinstance(avatarNameOrKey, int):
            avatarKey = str(avatarNameOrKey)
        if isinstance(avatarNameOrKey, str):
            avatarKey = next(
                (
                    k
                    for k, v in self.avatarConfig.items()
                    if str(v["AvatarName"]["Hash"]) in self.textMap
                    and self.textMap[str(v["AvatarName"]["Hash"])] == avatarNameOrKey
                ),
                None,
            )
        if selectKeys is None:
            # selectKeys = {"RankID", "Rank", "Name", "Desc", "SkillAddLevelList"}
            selectKeys = {"Rank", "Name", "Desc"}
        # 读取角色星魂列表
        rankList = []
        for rankID in self.avatarConfig[avatarKey]["RankIDList"]:
            rawRankConfig = self.avatarRankConfig[str(rankID)]  # 读取星魂配置
            rankConfig = {
                k: rawRankConfig[k]
                for k in selectKeys.intersection(rawRankConfig.keys())
            }
            rankConfig["Name"] = self.textMap[
                str(utils.get_stable_hash(rankConfig["Name"]))
            ]
            rankConfig["Desc"] = utils.processDesc(
                self.textMap[str(utils.get_stable_hash(rankConfig["Desc"]))],
                rawRankConfig["Param"],
            )
            rankList.append(rankConfig)
        return rankList

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
    def process_desc(desc, params):
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
    def replace_value_dict(value_dict):
        if isinstance(value_dict, dict):
            if "Value" in value_dict:
                return value_dict["Value"]
            else:
                return {k: utils.replace_value_dict(v) for k, v in value_dict.items()}
        elif isinstance(value_dict, list):
            return [utils.replace_value_dict(v) for v in value_dict]
        else:
            return value_dict
        
    @staticmethod
    def is_valid_promotion(level, promotion):
        flag = False

        if promotion == 0 and level >= 0 and level <= 20:
            flag = True
        elif promotion == 1 and level >= 20 and level <= 30:
            flag = True
        elif promotion == 2 and level >= 30 and level <= 40:
            flag = True
        elif promotion == 3 and level >= 40 and level <= 50:
            flag = True
        elif promotion == 4 and level >= 50 and level <= 80:
            flag = True
        elif promotion == 5 and level >= 60 and level <= 70:
            flag = True
        elif promotion == 6 and level >= 70 and level <= 80:
            flag = True

        return flag
    
    @staticmethod
    def get_valid_promotion(level, promotion):
        promotion == 6
        
        if level >= 0 and level <= 20:
            promotion == 0
        elif level > 20 and level <= 30:
            promotion == 1
        elif level > 30 and level <= 40:
            promotion == 2
        elif level > 40 and level <= 50:
            promotion == 3
        elif level > 50 and level <= 80:
            promotion == 4
        elif level > 60 and level <= 70:
            promotion == 5
        elif level > 70 and level <= 80:
            promotion == 6

        return promotion


class StarRailData:
    def __init__(self, language="CN"):
        self.language = language


    def load_data(self, path_to_starraildata):
        path_data_base = path_to_starraildata

        # 因为TextMap广泛使用，所以放在其他读取部分的前面，比较醒目
        text_map_file_name = "TextMap" + self.language + ".json"
        path_text_map = os.path.join(path_data_base, "TextMap", text_map_file_name)

        path_excel_output = os.path.join(path_data_base, "ExcelOutput")

        path_avatar_config = os.path.join(path_excel_output, "AvatarConfig.json")
        path_avatar_promotion_config = os.path.join(
            path_excel_output, "AvatarPromotionConfig.json"
        )
        path_avatar_skill_config = os.path.join(path_excel_output, "AvatarSkillConfig.json")
        path_avatar_skill_tree_config = os.path.join(
            path_excel_output, "AvatarSkillTreeConfig.json"
        )
        path_avatar_rank_config = os.path.join(path_excel_output, "AvatarRankConfig.json")
        path_extra_effect_config = os.path.join(path_excel_output, "ExtraEffectConfig.json")


        # read all json
        with open(path_text_map, "r", encoding="utf-8") as f:
            self.text_map = json.load(f)
        with open(path_avatar_config, "r", encoding="utf-8") as f:
            self.avatar_config = json.load(f)
        with open(path_avatar_promotion_config, "r", encoding="utf-8") as f:
            self.avatar_promotion_config = json.load(f)
        with open(path_avatar_skill_config, "r", encoding="utf-8") as f:
            self.avatar_skill_config = json.load(f)
        with open(path_avatar_skill_tree_config, "r", encoding="utf-8") as f:
            self.avatar_skill_tree_config = json.load(f)
        with open(path_avatar_rank_config, "r", encoding="utf-8") as f:
            self.avatar_rank_config = json.load(f)
        with open(path_extra_effect_config, "r", encoding="utf-8") as f:
            self.extra_effect_config = json.load(f)


    # 通过角色名获取角色ID
    def get_avatar_id_from_avatar_name(self, avatar_name_or_key):
        avatar_id_str = next(
                (
                    k
                    for k, v in self.avatar_config.items()
                    if str(v["AvatarName"]["Hash"]) in self.text_map
                    and self.text_map[str(v["AvatarName"]["Hash"])] == avatar_name_or_key
                ),
                None,
            )
        
        return avatar_id_str
    

    # 读取角色名列表
    def generate_avatar_name_list(self):
        return {
            k: self.text_map[str(self.avatar_config[k]["AvatarName"]["Hash"])]
            for k in self.avatar_config.keys()
        }
    

    def get_avatar_stat_list(self, avatar_id_str, level, promotion, select_keys):
        GROWTH_PROPERTY = [
            "Attack",
            "Defence",
            "HP",
        ]

        stat_list = []

        promotion_config = self.avatar_promotion_config[avatar_id_str][str(promotion)]
        for property_name in select_keys:
            if property_name not in GROWTH_PROPERTY:
                property_value = promotion_config[property_name]['Value']
            else:
                property_base_name = ''.join(property_name, 'Base')
                property_base_value = promotion_config[property_base_name]['Value']
                property_add_name = ''.join(property_name, 'Add')
                property_add_value = promotion_config[property_add_name]['Value']

                property_value = property_base_value + property_add_value * (level - 1)
       
            stat_list.append(property_value)

        return stat_list
    

    # 读取属性列表
    def generate_avatar_stat_list(self, avatar_name_or_key, level=80, promotion=6, select_keys=None):
        # 参数检查
        if isinstance(avatar_name_or_key, int):
            avatar_id_str = str(avatar_name_or_key)  # 转换为字符串
        if isinstance(avatar_name_or_key, str):
            # 封装成函数
            avatar_id_str = self.get_avatar_id_from_avatar_name(avatar_name_or_key)

        if not isinstance(level, int):
            warnings.warn("level must be a int, using default value 80")
            level = 80  # 不是整数，使用默认值
        elif level < 0 or level > 80:
            warnings.warn("Invalid value for level, using default value 80")
            level = 80  # 值不在范围内，使用默认值

        if not isinstance(promotion, int):
            warnings.warn("promotion must be a int, using default value 6")
            promotion = 6  # 不是整数，使用默认值
        elif promotion < 0 or promotion > 6:
            warnings.warn("Invalid value for promotion, using default value 6")
            promotion = 6  # 值不在范围内，使用默认值
        elif not utils.is_valid_promotion(level, promotion):
            warnings.warn("Promotion doesn't match level, using corresponding promotion")
            promotion = utils.get_valid_promotion(level, promotion)  # 值不在范围内，使用默认值

        if select_keys is None:
            select_keys = [
                "Attack",
                "Defence",
                "HP",
                "SpeedBase",
                "CriticalChance",
                "CriticalDamage",
                "BaseAggro"
            ]

        # 因为avatar_config数据都是用角色id作key，所以为了功能分离，将读取接口与实际读取模块进行分离。
        avatar_stat_list = self.get_avatar_stat_list(avatar_id_str, level, promotion, select_keys)

        return avatar_stat_list
    

    def get_avatar_skill_list(self, avatar_id_str, levels, select_keys):
        # 读取角色技能列表
        skill_list = []
        level_dict = {
            "Normal": levels[0],
            "BPSkill": levels[1],
            "Ultra": levels[2],
            "Maze": 1,
        }
        for skill_id in self.avatar_config[avatar_id_str]["SkillList"]:
            raw_skill_config = self.avatar_skill_config[str(skill_id)]  # 读取技能配置
            attack_type = raw_skill_config.get("1", {}).get("AttackType")  # 读取技能等级
            if attack_type == "MazeNormal":
                continue  # 不读取箱庭普攻
            level = level_dict.get(attack_type, levels[3])  # 读取对应等级
            raw_skill_config = raw_skill_config[str(level)]  # 选取需要的字段
            skill_config = {
                k: raw_skill_config[k]
                for k in select_keys.intersection(raw_skill_config.keys())
            }
            skill_config = {
                k: skill_config[k] for k in select_keys if k in skill_config.keys()
            }
            # 处理字段
            for key, value in skill_config.items():
                if isinstance(value, dict) and "Hash" in value:
                    if str(value["Hash"]) in self.text_map:
                        skill_config[key] = self.text_map[str(value["Hash"])]
                        if key == "SkillDesc" or key == "SimpleSkillDesc":
                            skill_config[key] = utils.process_desc(
                                skill_config[key], raw_skill_config["ParamList"]
                            )
                    else:  # 替换为空值
                        skill_config[key] = ""
            skill_config = utils.replace_value_dict(skill_config)
            skill_config = {k: v for k, v in skill_config.items() if v != ""}  # 删除空值
            skill_list.append(skill_config)

        return skill_list
    

    # 读取技能列表
    def generate_avatar_skill_list(self, avatar_name_or_key, levels=[6, 10, 10, 10], select_keys=None):
        # 参数检查
        if isinstance(avatar_name_or_key, int):
            avatar_id_str = str(avatar_name_or_key)  # 转换为字符串
        if isinstance(avatar_name_or_key, str):
            avatar_id_str = self.get_avatar_id_from_avatar_name(avatar_name_or_key)

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

        if select_keys is None:
            # select_keys = {"SkillID", "SkillName", "SkillTag", "SkillTypeDesc", "Level", "MaxLevel", "SkillDesc", "SimpleSkillDesc", "RatedSkillTreeID",\
            #       "RatedRankID", "ExtraEffectIDList", "SimpleExtraEffectIDList", "SPBase", "ParamList", "SimpleParamList", "StanceDamageType",\
            #       "AttackType", "SkillEffect", "SkillComboValueDelta"}
            # select_keys = {"SkillName", "SkillTag", "SkillTypeDesc", "Level", "MaxLevel", "SkillDesc", "SPBase"}
            select_keys = {
                "SkillName",
                "SkillTag",
                "SkillTypeDesc",
                "SkillDesc",
                "SPBase",
            }

        avatar_skill_list = self.get_avatar_skill_list(avatar_id_str, levels, select_keys)

        return avatar_skill_list
    
    
    def get_avatar_rank_list(self, avatar_id_str, select_keys):
        # 读取角色星魂列表
        rank_list = []
        for rankID in self.avatar_config[avatar_id_str]["RankIDList"]:
            raw_rank_config = self.avatar_rank_config[str(rankID)]  # 读取星魂配置
            rank_config = {
                k: raw_rank_config[k]
                for k in select_keys.intersection(raw_rank_config.keys())
            }
            rank_config["Name"] = self.text_map[
                str(utils.get_stable_hash(rank_config["Name"]))
            ]
            rank_config["Desc"] = utils.process_desc(
                self.text_map[str(utils.get_stable_hash(rank_config["Desc"]))],
                raw_rank_config["Param"],
            )
            rank_list.append(rank_config)
        return rank_list
    

    # 读取角色星魂(Rank)列表
    def generate_avatar_rank_list(self, avatar_name_or_key, select_keys=None):
        # 参数检查
        if isinstance(avatar_name_or_key, int):
            avatar_id_str = str(avatar_name_or_key)
        if isinstance(avatar_name_or_key, str):
            avatar_id_str = self.get_avatar_id_from_avatar_name(avatar_name_or_key)

        if select_keys is None:
            # select_keys = {"RankID", "Rank", "Name", "Desc", "SkillAddLevelList"}
            select_keys = {
                "Rank", 
                "Name", 
                "Desc"
            }

        avatar_rank_list = self.get_avatar_rank_list(avatar_id_str, select_keys)

        return avatar_rank_list
        
        

import pytest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.starraildatareader import create_star_rail_data

path_to_StarRailData = os.path.join(os.path.dirname(__file__), "..", "StarRailData")

answer = [
    {
        "SkillTag": "单攻",
        "SkillName": "极寒的弓矢",
        "SPBase": 19.999999686134988,
        "SkillTypeDesc": "普攻",
        "SkillDesc": "对指定敌方单体造成等同于三月七100%攻击力的冰属性伤害。",
    },
    {
        "SkillTag": "防御",
        "SkillName": "可爱即是正义",
        "SPBase": 29.999999529202483,
        "SkillTypeDesc": "战技",
        "SkillDesc": "为指定我方单体提供能够抵消等同于三月七57%防御力+760伤害的护盾，持续3回合。\\n若该目标当前生命值百分比大于等于30%，被敌方攻击的概率大幅提高。",
    },
    {
        "SkillTag": "群攻",
        "SkillName": "冰刻箭雨之时",
        "SPBase": 4.999999921533747,
        "SkillTypeDesc": "终结技",
        "SkillDesc": "对敌方全体造成等同于三月七150%攻击力的冰属性伤害。受到攻击的敌方目标有50%基础概率陷入冻结状态，持续1回合。\\n冻结状态下，敌方目标不能行动同时每回合开始时受到等同于三月七60%攻击力的冰属性附加伤害。",
    },
    {
        "SkillTag": "单攻",
        "SkillName": "少女的特权",
        "SPBase": 9.999999843067494,
        "SkillTypeDesc": "天赋",
        "SkillDesc": "当持有护盾的我方目标受到敌方目标攻击后，三月七立即向攻击者发起反击，对其造成等同于三月七100%攻击力的冰属性伤害，该效果每回合可触发2次。",
    },
    {
        "SkillName": "冻人的瞬间",
        "SkillTypeDesc": "秘技",
        "SkillDesc": "立即攻击敌人，进入战斗后有100%的基础概率使随机敌方单体陷入冻结状态，持续1回合。\\n冻结状态下，敌方目标不能行动同时每回合开始时受到等同于三月七50%攻击力的冰属性附加伤害。",
    },
]

# selectKeys = {"SkillID", "SkillName", "SkillTag", "SkillTypeDesc", "Level", "MaxLevel", "SkillDesc", "SimpleSkillDesc", "RatedSkillTreeID",\
#       "RatedRankID", "ExtraEffectIDList", "SimpleExtraEffectIDList", "SPBase", "ParamList", "SimpleParamList", "StanceDamageType",\
#       "AttackType", "SkillEffect", "SkillComboValueDelta"}
# selectKeys = {"SkillName", "SkillTag", "SkillTypeDesc", "Level", "MaxLevel", "SkillDesc", "SPBase"}
selectKeys = {"SkillName", "SkillTag", "SkillTypeDesc", "SkillDesc", "SPBase"}
starRailData = create_star_rail_data(path_to_StarRailData)


def test_getAvatarSkillListByName():
    avatarNameOrKey = "三月七"
    AvatarSkill = starRailData.getAvatarSkillList(
        avatarNameOrKey, levels=[6, 10, 10, 10], selectKeys=selectKeys
    )
    assert len(AvatarSkill) > 0
    assert AvatarSkill[0]["SkillTag"] == "单攻"


def test_getAvatarSkillListByID():
    avatarNameOrKey = 1001
    AvatarSkill = starRailData.getAvatarSkillList(
        avatarNameOrKey, levels=[6, 10, 10, 10], selectKeys=selectKeys
    )
    assert len(AvatarSkill) > 0
    assert AvatarSkill[0]["SkillTag"] == "单攻"
    
def test_getAvatarRankList():
    avatarNameOrKey = "三月七"
    AvatarRank = starRailData.getAvatarRankList(avatarNameOrKey)
    assert len(AvatarRank) > 0
    assert AvatarRank[0]["Name"] == "记忆中的你"
    assert AvatarRank[0]["Rank"] == 1
    assert AvatarRank[0]["Desc"] == "终结技每冻结1个目标，为三月七恢复6点能量。"


if __name__ == "__main__":
    pytest.main(["-s", "-v", __file__])

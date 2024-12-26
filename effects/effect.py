import asyncio

class Effect:
    @staticmethod
    async def ATKEffect(target, coefficient=1):
        print("딜버프 시작")
        prevATK = target.ATK
        target.ATK = target.ATK * coefficient  # 공격력 증가
        await asyncio.sleep(4)  # 4초 대기
        target.ATK = prevATK  # 원래 공격력 복원
        print("딜버프 끝")

    @staticmethod
    def apply_ATK_effect(target, coefficient=1):
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(Effect.ATKEffect(target, coefficient), loop=loop)

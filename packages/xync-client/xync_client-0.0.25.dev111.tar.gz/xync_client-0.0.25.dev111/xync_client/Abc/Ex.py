import logging
from abc import abstractmethod

import msgspec
from msgspec import Struct
from tortoise.exceptions import MultipleObjectsReturned, IntegrityError
from xync_schema import models
from xync_schema.types import CurEx, CoinEx, BaseAd, BaseAdIn

from xync_client.Abc.Base import BaseClient, MapOfIdsList
from xync_client.Abc.types import PmEx
from xync_client.TgWallet.pyro import PyroClient
from xync_client.loader import bot
from xync_client.pm_unifier import PmUnifier, PmUni


class BaseExClient(BaseClient):
    cur_map: dict[int, str] = {}
    unifier_class: type = PmUnifier

    @abstractmethod
    def pm_type_map(self, typ: models.Pmex) -> str: ...

    # 19: Список поддерживаемых валют тейкера
    @abstractmethod
    async def curs(self) -> dict[str, CurEx]:  # {cur.ticker: cur}
        ...

    # 20: Список платежных методов
    @abstractmethod
    async def pms(self, cur: models.Cur = None) -> dict[int | str, PmEx]:  # {pm.exid: pm}
        ...

    # 21: Список платежных методов по каждой валюте
    @abstractmethod
    async def cur_pms_map(self) -> MapOfIdsList:  # {cur.exid: [pm.exid]}
        ...

    # 22: Список торгуемых монет (с ограничениям по валютам, если есть)
    @abstractmethod
    async def coins(self) -> dict[str, CoinEx]:  # {coin.ticker: coin}
        ...

    # 23: Список пар валюта/монет
    @abstractmethod
    async def pairs(self) -> tuple[MapOfIdsList, MapOfIdsList]: ...

    # 24: Список объяв по (buy/sell, cur, coin, pm)
    @abstractmethod
    async def ads(
        self, coin_exid: str, cur_exid: str, is_sell: bool, pm_exids: list[str | int] = None, amount: int = None
    ) -> list[BaseAd]:  # {ad.id: ad}
        ...

    # 42: Чужая объява по id
    @abstractmethod
    async def ad(self, ad_id: int) -> BaseAd: ...

    # Преобразрование объекта объявления из формата биржи в формат xync
    @abstractmethod
    async def ad_epyd2pydin(self, ad: BaseAd) -> BaseAdIn: ...  # my_uid: for MyAd

    # 99: Страны
    async def countries(self) -> list[Struct]:
        return []

    # Импорт Pm-ов (с Pmcur-, Pmex- и Pmcurex-ами) и валют (с Curex-ами) с биржи в бд
    async def set_pmcurexs(self):
        PyroClient(bot)
        # Curs
        cur_pyds: dict[str, CurEx] = await self.curs()
        curs: dict[int | str, models.Cur] = {
            exid: (await models.Cur.update_or_create({"rate": cur_pyd.rate or 0}, ticker=cur_pyd.ticker))[0]
            for exid, cur_pyd in cur_pyds.items()
        }
        curexs = [
            models.Curex(**c.model_dump(exclude_none=True), cur=curs[c.exid], ex=self.ex) for c in cur_pyds.values()
        ]
        # Curex
        await models.Curex.bulk_create(
            curexs, update_fields=["minimum", "rounding_scale"], on_conflict=["cur_id", "ex_id"]
        )

        countries = await self.countries()

        for c in countries:
            if c.cur_id not in curs:
                cur, _ = await models.Cur.get_or_create(ticker=self.cur_map[c.cur_id])
                curs[cur.id] = cur
                c.cur_id = cur.id
            c.cur_id = curs[c.cur_id].id
        # Country preparing
        # countries = sorted(
        #     (c for c in countries if c.code not in (999, 9999, 441624, 999999)), key=lambda x: x.name
        # )  # sort and filter
        cnts = {
            "BosniaandHerzegovina": "BA",
            "Brunei": "BN",
            "Congo": "CD",
            "Djibouti": "DJ",
            "Guinea": "GN",
            "Iraq": "IQ",
            "Kyrgyzstan": "KG",
            "ComorosIslands": "KM",
            "Liberia": "LR",
            "Libya": "LY",
            "Yemen": "YE",
            "Zimbabwe": "ZW",
            "United States of America": "US",
            "Lebanon": "LB",
            "Central African Republic": "XA",
            "Laos": "LA",
            "Tanzania": "TZ",
            "Bangladesh": "BD",
        }
        [setattr(c, "short", cnts.get(c.name, c.short)) for c in countries]  # add missed shortNames
        # Countries create
        cntrs: [models.Country] = [models.Country(**msgspec.to_builtins(c)) for c in countries]
        # ids only for HTX
        await models.Country.bulk_create(cntrs, ignore_conflicts=True)
        # todo: curexcountry

        # Pms
        pms_epyds: dict[int | str, PmEx] = {
            k: v for k, v in sorted((await self.pms()).items(), key=lambda x: x[1].name)
        }  # sort by name
        pms: dict[int | str, models.Pm] = dict({})
        prev = 0, "", "", None  # id, normd-name, orig-name
        cntrs = [c.lower() for c in await models.Country.all().values_list("name", flat=True)]
        uni = self.unifier_class(cntrs)
        for k, pm in pms_epyds.items():
            pmu: PmUni = uni(pm.name)
            country_id = (
                await models.Country.get(name__iexact=cnt).values_list("id", flat=True)
                if (cnt := pmu.country)
                else None
            )
            if prev[2] == pm.name and pmu.country == prev[3]:  # оригинальное имя не уникально на этой бирже
                logging.warning(f"Pm: '{pm.name}' duplicated with ids {prev[0]}: {k} on {self.ex.name}")
                # новый Pm не добавляем, а берем старый с этим названием
                pm_ = pms.get(prev[0], await models.Pm.get_or_none(norm=prev[1], country_id=country_id))
                # и добавляем Pmex для него
                await models.Pmex.update_or_create({"name": pm.name}, ex=self.ex, exid=k, pm=pm_)
            elif (
                prev[1] == pmu.norm and pmu.country == prev[3]
            ):  # 2 разных оригинальных имени на этой бирже совпали при нормализации
                logging.error(
                    f"Pm: {pm.name}&{prev[2]} overnormd as {pmu.norm} with ids {prev[0]}: {k} on {self.ex.name}"
                )
                # новый Pm не добавляем, только Pmex для него
                # новый Pm не добавляем, а берем старый с этим названием
                pm_ = pms.get(prev[0], await models.Pm.get_or_none(norm=prev[1], country_id=country_id))
                # и добавляем.обновляем Pmex для него
                await models.Pmex.update_or_create({"pm": pm_}, ex=self.ex, exid=k, name=pm.name)
            else:
                pmin = models.Pm.validate({**pmu.model_dump(), "country_id": country_id, "typ": pm.typ})
                # # logo
                # if pm.logo and not await models.File.exists(name=pm.logo):
                #     if not pm.logo.startswith("https:"):
                #         if not pm.logo.startswith("/"):
                #             pm.logo = "/" + pm.logo
                #         pm.logo = "https://" + pm.logo
                #     async with ClientSession() as ss:
                #         resp = await ss.get(pm.logo)
                #         if resp.ok:
                #             byts = await resp.read()
                #             upf, ref = await pyro.save_file(byts, resp.content_type)
                #             await sleep(1)
                #             typ = FileType[resp.content_type.split("/")[-1]]
                #             file, _ = await models.File.update_or_create(
                #                 {"ref": ref, "size": len(byts), "typ": typ}, name=pm.logo
                #             )
                #             # fil = await pyro.get_file(file.ref)  # check
                #             pmin.logo_id = file.id
                # # /logo
                try:
                    pms[k], _ = await models.Pm.update_or_create(**pmin.df_unq())
                except (MultipleObjectsReturned, IntegrityError) as e:
                    raise e
            prev = k, pmu.norm, pm.name, pmu.country
        # Pmexs
        pmexs = [models.Pmex(exid=k, ex=self.ex, pm=pm, name=pms_epyds[k].name) for k, pm in pms.items()]
        await models.Pmex.bulk_create(pmexs, on_conflict=["ex_id", "exid"], update_fields=["pm_id", "name", "name_"])
        # Pmex banks
        for k, pm in pms_epyds.items():
            if banks := pm.banks:
                pmex = await models.Pmex.get(ex=self.ex, exid=k)  # pm=pms[k],
                for b in banks:
                    await models.PmexBank.update_or_create({"name": b.name}, exid=b.exid, pmex=pmex)

        cur2pms = await self.cur_pms_map()
        # # Link PayMethods with currencies
        pmcurs = set()
        for cur_id, exids in cur2pms.items():
            for exid in exids:
                if not (pm_id := pms.get(exid) and pms[exid].id):
                    if pmex := await models.Pmex.get_or_none(ex=self.ex, exid=exid):
                        pm_id = pmex.pm_id
                    else:
                        logging.critical(f"For cur {cur_id} not found pm#{exid}")
                        continue
                pmcurs.add((await models.Pmcur.update_or_create(cur=curs[cur_id], pm_id=pm_id))[0])
        # pmcurexs = [Pmcurex(pmcur=pmcur, ex=self.ex) for pmcur in pmcurs]
        # await Pmcurex.bulk_create(pmcurexs)

    # Импорт монет (с Coinex-ами) с биржи в бд
    async def set_coinexs(self):
        coins: dict[str, CoinEx] = await self.coins()
        coins_db: dict[int, models.Coin] = {
            c.exid: (await models.Coin.update_or_create(ticker=c.ticker))[0] for c in coins.values()
        }
        coinexs: list[models.Coinex] = [
            models.Coinex(coin=coins_db[c.exid], ex=self.ex, exid=c.exid, minimum=c.minimum) for c in coins.values()
        ]
        await models.Coinex.bulk_create(coinexs, update_fields=["minimum"], on_conflict=["coin_id", "ex_id"])

    # Импорт пар биржи в бд
    async def set_pairs(self):
        curs: dict[str, CurEx] = {
            k: (await models.Cur.get_or_create(ticker=c.ticker))[0] for k, c in (await self.curs()).items()
        }
        coins: dict[str, CoinEx] = {
            k: (await models.Coin.get_or_create(ticker=c.ticker))[0] for k, c in (await self.coins()).items()
        }
        prs: tuple[dict, dict] = await self.pairs()
        for is_sell in (0, 1):
            dirs: list[models.Direction] = []
            for cur, coinz in prs[is_sell].items():
                for coin in coinz:
                    pair, _ = await models.Pair.get_or_create(coin=coins[coin], cur=curs[cur])
                    pairex, _ = await models.PairEx.get_or_create(pair=pair, ex=self.ex)
                    dirs += [models.Direction(sell=is_sell, pairex=pairex)]
            await models.Direction.bulk_create(dirs, ignore_conflicts=True)

    # Сохранение чужого объявления (с Pm-ами) в бд
    async def ad_pydin2db(self, ad_pydin: BaseAdIn) -> models.Ad:
        ad_in = models.Ad.validate(ad_pydin.model_dump())
        ad_db, _ = await models.Ad.update_or_create(**ad_in.df_unq())
        if getattr(ad_pydin, "pms_", None):  # if it ListItem, not Full One # todo: remove?
            await ad_db.pms.add(*ad_pydin.pms_)
        return ad_db

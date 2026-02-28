"""Scene definitions for the gerrymandering story map."""

from __future__ import annotations

from llmaps.components import Scene, SceneComparison

# ── Colors (shared with build_map.py) ──
DEM_COLOR = "#2166ac"
REP_COLOR = "#b2182b"

# ── Coordinates ──
PA_CENTER = [-77.53413, 41.01974]
PA_ZOOM = 6.92
PHILLY_CENTER = [-75.15, 40.0]
GOOFY_CENTER = [-75.63987, 40.07844]
GOOFY_ZOOM = 8.95
PHILLY_SUBURBS = [-75.55869, 40.16528]
PHILLY_SUBURBS_ZOOM = 8.58

# ── Popup config ──
POPUP_FIELDS = [
    "district",
    "year",
    "winner",
    "dem_votes",
    "rep_votes",
    "dem_pct",
    "rep_pct",
    "margin",
]

POPUP_LABELS = {
    "district": "Округ",
    "year": "Год",
    "winner": "Победитель",
    "dem_votes": "Голоса D",
    "rep_votes": "Голоса R",
    "dem_pct": "D, %",
    "rep_pct": "R, %",
    "margin": "Разрыв, п.п.",
}


# ── Scenes ──
SCENES = [
    Scene(
        id="intro",
        title="Что такое джерримендеринг?",
        content=f"""
<p>Представь: в твоём городе <strong>50 избирателей</strong>. 60% голосуют за
<span style="color:{DEM_COLOR}">синих</span>, 40 — за
<span style="color:{REP_COLOR}">красных</span>.</p>
<p>Нужно поделить город на 5 округов по 10 человек. Честный вариант: синие
побеждают в 3 округах. Всё справедливо.</p>
<p>Но что, если линии округов рисуют <strong>сами красные</strong>?
Они могут <em>упаковать</em> всех синих в 1–2 округа — синие выигрывают там
с огромным перевесом, но их голоса тратятся впустую.</p>
<p><strong>Итог: 60% голосов → 2 места. 40% голосов → 3 места.</strong></p>
<p>Это и есть джерримендеринг: тот, кто рисует карту, решает, кто победит.</p>
<p>Такая схема характерна для стран с <strong>мажоритарной системой в одномандатных округах</strong>
(как в США): там границы округов напрямую влияют на результат выборов.</p>
<p style="margin-top: 1rem; font-size: 0.8em; color: #888;">
Источник: <a href="https://en.wikipedia.org/wiki/Gerrymandering_in_the_United_States" target="_blank" style="color:#888;">Gerrymandering in the United States</a></p>
""",
        center=PA_CENTER,
        zoom=PA_ZOOM,
    ),
    Scene(
        id="tools",
        title="Два инструмента: packing и cracking",
        content="""
<p><strong>Packing (упаковка)</strong> — концентрируешь противников в один округ.
Они выигрывают 80–90%, но это одно место. Остальная сила потрачена впустую.</p>
<p><strong>Cracking (дробление)</strong> — оставшихся размазываешь тонким слоем
по многим округам, где они везде чуть в меньшинстве — и нигде не побеждают.</p>
<p>Комбинация этих приёмов позволяет превратить меньшинство
в большинство в парламенте.</p>
<p style="margin-top: 1rem; font-size: 0.8em; color: #888;">
Источник: <a href="https://en.wikipedia.org/wiki/Gerrymandering_in_the_United_States" target="_blank" style="color:#888;">packing и cracking</a></p>
""",
        center=PA_CENTER,
        zoom=PA_ZOOM,
    ),
    Scene(
        id="pa_context",
        title="Пенсильвания, 2010 год",
        content=f"""
<p>После переписи населения каждые 10 лет штаты перекраивают границы округов.</p>
<p>В 2010 году <span style="color:{REP_COLOR}"><strong>республиканцы</strong></span>
выиграли выборы в законодательное собрание Пенсильвании — и получили право
рисовать карту 18 конгрессменов на следующие 10 лет.</p>
<p>Они воспользовались этим шансом по полной.</p>
<p style="margin-top: 1rem; font-size: 0.8em; color: #888;">
Источник: <a href="https://en.wikipedia.org/wiki/Redistricting_in_Pennsylvania" target="_blank" style="color:#888;">Redistricting in Pennsylvania</a></p>
""",
        center=PA_CENTER,
        zoom=PA_ZOOM,
        visible_layers=["fill-2016"],
    ),
    Scene(
        id="map_2016",
        title="Карта 2011 года — результаты выборов 2016",
        content=f"""
<p>Вот карта, которую нарисовали республиканцы. Каждый округ закрашен по цвету
победившей партии:</p>
<p><span style="color:{DEM_COLOR}">■</span> демократы &nbsp;
<span style="color:{REP_COLOR}">■</span> республиканцы</p>
<p>Обратите внимание на <strong>причудливые формы</strong> округов —
они нарисованы не для удобства жителей, а для максимального
политического преимущества.</p>
""",
        center=PA_CENTER,
        zoom=PA_ZOOM,
        visible_layers=["fill-2016"],
    ),
    Scene(
        id="goofy",
        title="«Гуфи пинает Дональда Дака» — округ №7",
        content=f"""
<p>Округ 7 стал символом этого безумия. Washington Post провёл конкурс на лучшее
название его формы — победило: <strong>«Гуфи пинает Дональда Дака»</strong>.</p>
<p>Округ растянулся на 80 км через пять каунти. В самом узком месте
его можно было пересечь буквально за полминуты: Усэйн Болт пробежал бы его очень быстро.</p>
<p>Зачем? Чтобы включить нужные предместья Филадельфии с республиканскими
избирателями и обойти демократические анклавы.</p>
<p>Результат: <span style="color:{REP_COLOR}"><strong>республиканец победил
59% против 40%</strong></span>.</p>
<p style="margin-top: 1rem; font-size: 0.8em; color: #888;">
Источники: <a href="https://www.washingtonpost.com/blogs/the-fix/post/name-that-district-contest-winner-goofy-kicking-donald-duck/2011/12/29/gIQA2Fa2OP_blog.html" target="_blank" style="color:#888;">Washington Post</a>,
<a href="https://en.wikipedia.org/wiki/Pennsylvania%27s_7th_congressional_district" target="_blank" style="color:#888;">PA-7 district</a></p>
""",
        center=GOOFY_CENTER,
        zoom=GOOFY_ZOOM,
        comparison=SceneComparison(
            before_layers=["fill-2016"],
            after_layers=["fill-2016"],
            before_highlight={"pa-2016": [7]},
            after_highlight={"pa-2016": [7]},
        ),
    ),
    Scene(
        id="packing",
        title="Packing: демократы упакованы",
        content=f"""
<p>Посмотрите на <span style="color:{DEM_COLOR}"><strong>синие округа</strong></span>
вокруг Филадельфии — округа 1, 2 и 13.</p>
<p>Демократы здесь побеждают с гигантскими отрывами:</p>
<ul>
<li>Округ 1: <strong>82%</strong></li>
<li>Округ 2: <strong>90%</strong></li>
<li>Округ 13: <strong>100%</strong> (без соперника!)</li>
</ul>
<p>Все эти голоса «сгорают» — для победы достаточно 50%, но у демократов
по 80–100%. Это и есть <strong>packing</strong>.</p>
<p style="margin-top: 1rem; font-size: 0.8em; color: #888;">
Источник: <a href="https://en.wikipedia.org/wiki/2016_United_States_House_of_Representatives_elections_in_Pennsylvania" target="_blank" style="color:#888;">PA elections 2016</a></p>
""",
        center=PHILLY_CENTER,
        zoom=9.5,
        visible_layers=["fill-2016"],
        highlight={"pa-2016": [1, 2, 13]},
    ),
    Scene(
        id="cracking",
        title="Cracking: пригороды раздроблены",
        content="""
<p>А вот пригородные округа 6, 7 и 8 — тут демократов тоже немало,
но их аккуратно <strong>раздробили</strong> между округами.</p>
<p>Республиканцы выигрывают каждый с комфортным, но не огромным перевесом:</p>
<ul>
<li>Округ 6: R <strong>57%</strong> — D 43%</li>
<li>Округ 7: R <strong>59%</strong> — D 41%</li>
<li>Округ 8: R <strong>54%</strong> — D 46%</li>
</ul>
<p>Это <strong>cracking</strong> — размазать оппозицию так, чтобы
нигде не набиралось большинство.</p>
<p style="margin-top: 1rem; font-size: 0.8em; color: #888;">
Источник: <a href="https://en.wikipedia.org/wiki/2016_United_States_House_of_Representatives_elections_in_Pennsylvania" target="_blank" style="color:#888;">PA elections 2016</a></p>
""",
        center=PHILLY_SUBURBS,
        zoom=PHILLY_SUBURBS_ZOOM,
        visible_layers=["fill-2016"],
        highlight={"pa-2016": [6, 7, 8]},
    ),
    Scene(
        id="results_2016",
        title="Итог 2016: 45% голосов → 28% мест",
        content=f"""
<p>Если считать <strong>фактические голоса по всему штату</strong> (сумма голосов во всех 18 округах),
пропорция была такой:</p>
<p><span style="color:{DEM_COLOR}"><strong>Демократы: 45.7% голосов →
5 мест из 18 (28%)</strong></span></p>
<p><span style="color:{REP_COLOR}"><strong>Республиканцы: 53.9% голосов →
13 мест из 18 (72%)</strong></span></p>
<p>Разрыв между долей голосов и долей мест — визитная карточка
джерримендеринга. Система работала идеально — для тех,
кто её нарисовал.</p>
<p style="margin-top: 1rem; font-size: 0.8em; color: #888;">
Источник: <a href="https://en.wikipedia.org/wiki/2016_United_States_House_of_Representatives_elections_in_Pennsylvania" target="_blank" style="color:#888;">PA elections 2016</a></p>
""",
        center=PA_CENTER,
        zoom=PA_ZOOM,
        visible_layers=["fill-2016"],
    ),
    Scene(
        id="court",
        title="Суд: карта неконституционна",
        content="""
<p>В январе 2018 года <strong>Верховный суд Пенсильвании</strong> признал
карту 2011 года неконституционной.</p>
<p>Дело: <em>League of Women Voters v. Commonwealth of Pennsylvania</em>.</p>
<p>Суд постановил: карта нарушает Статью I Конституции штата
о свободных и честных выборах.</p>
<p>Республиканское законодательное собрание не смогло согласовать новую карту
до дедлайна, установленного судом.
Тогда <strong>суд нарисовал карту сам</strong>.</p>
<p style="margin-top: 1rem; font-size: 0.8em; color: #888;">
Источник: <a href="https://en.wikipedia.org/wiki/League_of_Women_Voters_of_Pennsylvania_v._Commonwealth_of_Pennsylvania" target="_blank" style="color:#888;">League of Women Voters v. Commonwealth of Pennsylvania</a></p>
""",
        center=PA_CENTER,
        zoom=PA_ZOOM,
        visible_layers=["fill-2016"],
    ),
    Scene(
        id="map_2018",
        title="Новая карта 2018 года",
        content=f"""
<p>Вот карта, нарисованная судом. Сравните с предыдущей:</p>
<p>Округа стали <strong>компактными</strong> и <strong>географически
логичными</strong>. Никаких «Гуфи» — чёткие границы, следующие
границам каунти.</p>
<p><span style="color:{DEM_COLOR}">■</span> демократы &nbsp;
<span style="color:{REP_COLOR}">■</span> республиканцы</p>
<p style="margin-top: 1rem; font-size: 0.8em; color: #888;">
Источник: <a href="https://en.wikipedia.org/wiki/League_of_Women_Voters_of_Pennsylvania_v._Commonwealth_of_Pennsylvania" target="_blank" style="color:#888;">решение Верховного суда PA (2018)</a></p>
""",
        center=PA_CENTER,
        zoom=PA_ZOOM,
        comparison=SceneComparison(
            before_layers=["fill-2016"],
            after_layers=["fill-2018"],
            before_label="2016",
            after_label="2018",
        ),
    ),
    Scene(
        id="new_d7",
        title="Что стало с «Гуфи»-территорией",
        content=f"""
    <p>После решения суда территорию старого «Гуфи»-округа в основном
    разделили между новыми округами <strong>5</strong> и <strong>6</strong>
    (частично — 4).</p>
    <p>Результаты 2018: <span style="color:{DEM_COLOR}"><strong>округ 5 — 65%</strong></span>,
    <span style="color:{DEM_COLOR}"><strong>округ 6 — 59%</strong></span> за демократов.</p>
    <p>Когда границы становятся компактнее и логичнее, карта меньше искажает
    реальную политическую географию региона.</p>
    <p style="margin-top: 1rem; font-size: 0.8em; color: #888;">
    Источники: <a href="https://en.wikipedia.org/wiki/Pennsylvania%27s_7th_congressional_district" target="_blank" style="color:#888;">история старого PA-7</a>,
    <a href="https://en.wikipedia.org/wiki/2018_United_States_House_of_Representatives_elections_in_Pennsylvania" target="_blank" style="color:#888;">PA elections 2018</a></p>
""",
        center=GOOFY_CENTER,
        zoom=GOOFY_ZOOM,
        comparison=SceneComparison(
            before_layers=["fill-2016"],
            after_layers=["fill-2018"],
            before_label="2016",
            after_label="2018",
            before_highlight={"pa-2016": [7]},
            after_highlight={"pa-2018": [5, 6]},
        ),
    ),
    Scene(
        id="results_2018",
        title="Итог 2018: справедливое представительство",
        content=f"""
<p>Результат 2018 года:</p>
<p><span style="color:{DEM_COLOR}"><strong>Демократы: 54.9% голосов →
9 мест из 18 (50%)</strong></span></p>
<p><span style="color:{REP_COLOR}"><strong>Республиканцы: 44.7% голосов →
9 мест из 18 (50%)</strong></span></p>
<p>Представительство стало заметно справедливее: разрыв между долей голосов
и долей мест резко сократился по сравнению с 2016 годом.</p>
<p style="margin-top: 1rem; font-size: 0.8em; color: #888;">
Источник: <a href="https://en.wikipedia.org/wiki/2018_United_States_House_of_Representatives_elections_in_Pennsylvania" target="_blank" style="color:#888;">PA elections 2018</a></p>
""",
        center=PA_CENTER,
        zoom=PA_ZOOM,
        visible_layers=["fill-2018"],
    ),
    Scene(
        id="conclusion",
        title="Те же люди — другая карта",
        content="""
<p><strong>Карта — не нейтральный инструмент.</strong> В 2016 году она превращала
45.7% голосов демократов в 28% мест. После судебной реформы карты
искажение стало значительно меньше.</p>
<p>Джерримендеринг — это когда выбирают не избиратели политиков,
а политики — своих избирателей.</p>
<p style="margin-top: 1.5rem; font-size: 0.85em; color: #888;">
Источники:
<a href="https://en.wikipedia.org/wiki/League_of_Women_Voters_of_Pennsylvania_v._Commonwealth_of_Pennsylvania" target="_blank" style="color:#888;">LWV v. Commonwealth of Pennsylvania (2018)</a>,
<a href="https://www.census.gov/" target="_blank" style="color:#888;">US Census Bureau</a>,
<a href="https://en.wikipedia.org/wiki/2016_United_States_House_of_Representatives_elections_in_Pennsylvania" target="_blank" style="color:#888;">PA elections 2016</a></p>
""",
        center=PA_CENTER,
        zoom=PA_ZOOM,
        visible_layers=["fill-2018"],
    ),
]

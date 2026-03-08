"""Localized text content for the gerrymandering story map."""

from __future__ import annotations

SCENE_ORDER = [
    "intro",
    "tools",
    "pa_context",
    "map_2016",
    "goofy",
    "packing",
    "cracking",
    "results_2016",
    "court",
    "map_2018",
    "new_d7",
    "results_2018",
    "conclusion",
]

TEXTS = {
    "en": {
        "map_title": "Gerrymandering in Pennsylvania",
        "comparison_slider_hint": "Drag the slider to compare",
        "scroll_hints": {
            "scroll_down": "Keep scrolling",
            "next_wheel": "Scroll to continue",
            "next_swipe": "Scroll once more",
        },
        "popup_labels": {
            "district": "District",
            "year": "Year",
            "winner": "Winner",
            "dem_votes": "Dem votes",
            "rep_votes": "Rep votes",
            "dem_pct": "Dem, %",
            "rep_pct": "Rep, %",
            "margin": "Margin, p.p.",
        },
        "scenes": {
            "intro": {
                "title": "What is gerrymandering?",
                "content": """
<p>Imagine a city with <strong>50 voters</strong>. 60% vote
for <span style=\"color:{DEM_COLOR}\">blue</span>, 40% for
<span style=\"color:{REP_COLOR}\">red</span>.</p>
<p>You need 5 districts with 10 people each. In a fair map, blue wins
3 districts. That is proportional.</p>
<p>But if <strong>red politicians</strong> draw district lines,
they can <em>pack</em> many blue voters into 1–2 districts, where blue wins
by huge margins and wastes votes.</p>
<p><strong>Result: 60% of votes → 2 seats. 40% of votes → 3 seats.</strong></p>
<p>That is gerrymandering: the mapmaker can shape the winner.</p>
<p>This is especially powerful in <strong>single-member district systems</strong>
(like the U.S. House), where boundaries directly affect outcomes.</p>
<p style=\"margin-top: 1rem; font-size: 0.8em; color: #888;\">
Source: <a href=\"https://en.wikipedia.org/wiki/Gerrymandering_in_the_United_States\" target=\"_blank\" style=\"color:#888;\">Gerrymandering in the United States</a></p>
""",
            },
            "tools": {
                "title": "Two tools: packing and cracking",
                "content": """
<p><strong>Packing</strong> means concentrating opposition voters in one district.
They might win 80–90%, but only get one seat.</p>
<p><strong>Cracking</strong> means splitting the rest across many districts,
so they are just short of a majority everywhere.</p>
<p>Together, these tactics can turn a statewide minority
into a legislative majority.</p>
<p style=\"margin-top: 1rem; font-size: 0.8em; color: #888;\">
Source: <a href=\"https://en.wikipedia.org/wiki/Gerrymandering_in_the_United_States\" target=\"_blank\" style=\"color:#888;\">packing and cracking</a></p>
""",
            },
            "pa_context": {
                "title": "Pennsylvania, 2010",
                "content": """
<p>After each census, states redraw congressional districts every 10 years.</p>
<p>In 2010, <span style=\"color:{REP_COLOR}\"><strong>Republicans</strong></span>
won the Pennsylvania legislature and gained control over the 18-district map
for the next decade.</p>
<p>They used that power aggressively.</p>
<p style=\"margin-top: 1rem; font-size: 0.8em; color: #888;\">
Source: <a href=\"https://en.wikipedia.org/wiki/Redistricting_in_Pennsylvania\" target=\"_blank\" style=\"color:#888;\">Redistricting in Pennsylvania</a></p>
""",
            },
            "map_2016": {
                "title": "2011 map — 2016 election results",
                "content": """
<p>This is the map drawn by Republicans. Each district is colored by the winning party:</p>
<p><span style=\"color:{DEM_COLOR}\">■</span> Democrats &nbsp;
<span style=\"color:{REP_COLOR}\">■</span> Republicans</p>
<p>Notice the <strong>odd district shapes</strong>.
They were not designed for coherent communities, but for political advantage.</p>
""",
            },
            "goofy": {
                "title": "\"Goofy kicks Donald Duck\" — District 7",
                "content": """
<p>District 7 became the symbol of this map. The Washington Post held a naming contest,
and the winner was <strong>\"Goofy kicking Donald Duck\"</strong>.</p>
<p>The district stretched about 80 km across five counties. At one narrow point,
you could cross it in under a minute.</p>
<p>Why? To include selected Republican-leaning Philadelphia suburbs
while bypassing Democratic pockets.</p>
<p>Outcome: <span style=\"color:{REP_COLOR}\"><strong>Republican wins
59% to 40%</strong></span>.</p>
<p style=\"margin-top: 1rem; font-size: 0.8em; color: #888;\">
Sources: <a href=\"https://www.washingtonpost.com/blogs/the-fix/post/name-that-district-contest-winner-goofy-kicking-donald-duck/2011/12/29/gIQA2Fa2OP_blog.html\" target=\"_blank\" style=\"color:#888;\">Washington Post</a>,
<a href=\"https://en.wikipedia.org/wiki/Pennsylvania%27s_7th_congressional_district\" target=\"_blank\" style=\"color:#888;\">PA-7 district</a></p>
""",
            },
            "packing": {
                "title": "Packing: Democrats are concentrated",
                "content": """
<p>Look at the <span style=\"color:{DEM_COLOR}\"><strong>blue districts</strong></span>
near Philadelphia — districts 1, 2, and 13.</p>
<p>Democrats won there by huge margins:</p>
<ul>
<li>District 1: <strong>82%</strong></li>
<li>District 2: <strong>90%</strong></li>
<li>District 13: <strong>100%</strong> (uncontested)</li>
</ul>
<p>Those excess votes are "wasted" — only 50%+ is needed to win a seat.
That is <strong>packing</strong>.</p>
<p style=\"margin-top: 1rem; font-size: 0.8em; color: #888;\">
Source: <a href=\"https://en.wikipedia.org/wiki/2016_United_States_House_of_Representatives_elections_in_Pennsylvania\" target=\"_blank\" style=\"color:#888;\">PA elections 2016</a></p>
""",
            },
            "cracking": {
                "title": "Cracking: suburbs are split",
                "content": """
<p>Now look at suburban districts 6, 7, and 8. Democrats were present,
but carefully <strong>split</strong> across districts.</p>
<p>Republicans won each seat with comfortable, not massive, margins:</p>
<ul>
<li>District 6: R <strong>57%</strong> — D 43%</li>
<li>District 7: R <strong>59%</strong> — D 41%</li>
<li>District 8: R <strong>54%</strong> — D 46%</li>
</ul>
<p>This is <strong>cracking</strong> — spreading opposition voters so they
cannot form a majority anywhere.</p>
<p style=\"margin-top: 1rem; font-size: 0.8em; color: #888;\">
Source: <a href=\"https://en.wikipedia.org/wiki/2016_United_States_House_of_Representatives_elections_in_Pennsylvania\" target=\"_blank\" style=\"color:#888;\">PA elections 2016</a></p>
""",
            },
            "results_2016": {
                "title": "2016 result: 45% votes → 28% seats",
                "content": """
<p>Using <strong>actual statewide vote totals</strong> (sum across all 18 districts):</p>
<p><span style=\"color:{DEM_COLOR}\"><strong>Democrats: 45.7% of votes →
5 of 18 seats (28%)</strong></span></p>
<p><span style=\"color:{REP_COLOR}\"><strong>Republicans: 53.9% of votes →
13 of 18 seats (72%)</strong></span></p>
<p>The gap between vote share and seat share is a classic gerrymandering signal.</p>
<p style=\"margin-top: 1rem; font-size: 0.8em; color: #888;\">
Source: <a href=\"https://en.wikipedia.org/wiki/2016_United_States_House_of_Representatives_elections_in_Pennsylvania\" target=\"_blank\" style=\"color:#888;\">PA elections 2016</a></p>
""",
            },
            "court": {
                "title": "Court: map is unconstitutional",
                "content": """
<p>In January 2018, the <strong>Pennsylvania Supreme Court</strong>
ruled that the 2011 map was unconstitutional.</p>
<p>Case: <em>League of Women Voters v. Commonwealth of Pennsylvania</em>.</p>
<p>The court held that the map violated Article I of the state constitution,
which guarantees free and equal elections.</p>
<p>The legislature failed to agree on a replacement map by the court deadline,
so the <strong>court imposed a new map</strong>.</p>
<p style=\"margin-top: 1rem; font-size: 0.8em; color: #888;\">
Source: <a href=\"https://en.wikipedia.org/wiki/League_of_Women_Voters_of_Pennsylvania_v._Commonwealth_of_Pennsylvania\" target=\"_blank\" style=\"color:#888;\">League of Women Voters v. Commonwealth of Pennsylvania</a></p>
""",
            },
            "map_2018": {
                "title": "New map in 2018",
                "content": """
<p>This is the court-drawn map. Compare it to the old one.</p>
<p>Districts became more <strong>compact</strong> and geographically coherent.
No more "Goofy" shape.</p>
<p><span style=\"color:{DEM_COLOR}\">■</span> Democrats &nbsp;
<span style=\"color:{REP_COLOR}\">■</span> Republicans</p>
<p style=\"margin-top: 1rem; font-size: 0.8em; color: #888;\">
Source: <a href=\"https://en.wikipedia.org/wiki/League_of_Women_Voters_of_Pennsylvania_v._Commonwealth_of_Pennsylvania\" target=\"_blank\" style=\"color:#888;\">PA Supreme Court remedy (2018)</a></p>
""",
            },
            "new_d7": {
                "title": "What happened to the “Goofy” area",
                "content": """
<p>After the ruling, most of the old "Goofy" district area
was reassigned into new districts <strong>5</strong> and <strong>6</strong>
(with some parts in 4).</p>
<p>2018 results there: <span style=\"color:{DEM_COLOR}\"><strong>District 5 — 65%</strong></span>,
<span style=\"color:{DEM_COLOR}\"><strong>District 6 — 59%</strong></span> for Democrats.</p>
<p>When boundaries are more compact and logical,
the map better reflects the region's real political geography.</p>
<p style=\"margin-top: 1rem; font-size: 0.8em; color: #888;\">
Sources: <a href=\"https://en.wikipedia.org/wiki/Pennsylvania%27s_7th_congressional_district\" target=\"_blank\" style=\"color:#888;\">history of old PA-7</a>,
<a href=\"https://en.wikipedia.org/wiki/2018_United_States_House_of_Representatives_elections_in_Pennsylvania\" target=\"_blank\" style=\"color:#888;\">PA elections 2018</a></p>
""",
            },
            "results_2018": {
                "title": "2018 result: fairer representation",
                "content": """
<p>2018 statewide outcome:</p>
<p><span style=\"color:{DEM_COLOR}\"><strong>Democrats: 54.9% of votes →
9 of 18 seats (50%)</strong></span></p>
<p><span style=\"color:{REP_COLOR}\"><strong>Republicans: 44.7% of votes →
9 of 18 seats (50%)</strong></span></p>
<p>Representation became much fairer than in 2016:
seat share moved closer to vote share.</p>
<p style=\"margin-top: 1rem; font-size: 0.8em; color: #888;\">
Source: <a href=\"https://en.wikipedia.org/wiki/2018_United_States_House_of_Representatives_elections_in_Pennsylvania\" target=\"_blank\" style=\"color:#888;\">PA elections 2018</a></p>
""",
            },
            "conclusion": {
                "title": "Same people — different map",
                "content": """
<p><strong>A map is not neutral.</strong> In 2016, it turned
45.7% Democratic votes into 28% of seats. After judicial redistricting,
the distortion dropped sharply.</p>
<p>Gerrymandering means voters do not choose politicians —
politicians choose their voters.</p>
<p style=\"margin-top: 1.5rem; font-size: 0.85em; color: #888;\">
Sources:
<a href=\"https://en.wikipedia.org/wiki/League_of_Women_Voters_of_Pennsylvania_v._Commonwealth_of_Pennsylvania\" target=\"_blank\" style=\"color:#888;\">LWV v. Commonwealth of Pennsylvania (2018)</a>,
<a href=\"https://www.census.gov/\" target=\"_blank\" style=\"color:#888;\">US Census Bureau</a>,
<a href=\"https://en.wikipedia.org/wiki/2016_United_States_House_of_Representatives_elections_in_Pennsylvania\" target=\"_blank\" style=\"color:#888;\">PA elections 2016</a></p>
""",
            },
        },
        "grid": {
            "voters": "voters",
            "blue_pct": "blue",
            "red_pct": "red",
            "fair_division": "Fair division",
            "gerrymandering": "Gerrymandering",
            "blue_count": "blue",
            "red_count": "red",
            "minority_wins": "Minority wins!",
            "same_people": "Same 50 people, same lines",
            "votes_by_district": "Votes by district:",
            "district_prefix": "District",
        },
    },
    "ru": {
        "map_title": "Джерримендеринг в Пенсильвании",
        "comparison_slider_hint": "Потяните слайдер для сравнения",
        "scroll_hints": {
            "scroll_down": "Листайте дальше",
            "next_wheel": "Прокрутите, чтобы продолжить",
            "next_swipe": "Прокрутите ещё раз",
        },
        "popup_labels": {
            "district": "Округ",
            "year": "Год",
            "winner": "Победитель",
            "dem_votes": "Голоса D",
            "rep_votes": "Голоса R",
            "dem_pct": "D, %",
            "rep_pct": "R, %",
            "margin": "Разрыв, п.п.",
        },
        "scenes": {
            "intro": {
                "title": "Что такое джерримендеринг?",
                "content": """
<p>Представь: в твоём городе <strong>50 избирателей</strong>. 60% голосуют за
<span style=\"color:{DEM_COLOR}\">синих</span>, 40 — за
<span style=\"color:{REP_COLOR}\">красных</span>.</p>
<p>Нужно поделить город на 5 округов по 10 человек. Честный вариант: синие
побеждают в 3 округах. Всё справедливо.</p>
<p>Но что, если линии округов рисуют <strong>сами красные</strong>?
Они могут <em>упаковать</em> всех синих в 1–2 округа — синие выигрывают там
с огромным перевесом, но их голоса тратятся впустую.</p>
<p><strong>Итог: 60% голосов → 2 места. 40% голосов → 3 места.</strong></p>
<p>Это и есть джерримендеринг: тот, кто рисует карту, решает, кто победит.</p>
<p>Такая схема характерна для стран с <strong>мажоритарной системой в одномандатных округах</strong>
(как в США): там границы округов напрямую влияют на результат выборов.</p>
<p style=\"margin-top: 1rem; font-size: 0.8em; color: #888;\">
Источник: <a href=\"https://en.wikipedia.org/wiki/Gerrymandering_in_the_United_States\" target=\"_blank\" style=\"color:#888;\">Gerrymandering in the United States</a></p>
""",
            },
            "tools": {
                "title": "Два инструмента: packing и cracking",
                "content": """
<p><strong>Packing (упаковка)</strong> — концентрируешь противников в один округ.
Они выигрывают 80–90%, но это одно место. Остальная сила потрачена впустую.</p>
<p><strong>Cracking (дробление)</strong> — оставшихся размазываешь тонким слоем
по многим округам, где они везде чуть в меньшинстве — и нигде не побеждают.</p>
<p>Комбинация этих приёмов позволяет превратить меньшинство
в большинство в парламенте.</p>
<p style=\"margin-top: 1rem; font-size: 0.8em; color: #888;\">
Источник: <a href=\"https://en.wikipedia.org/wiki/Gerrymandering_in_the_United_States\" target=\"_blank\" style=\"color:#888;\">packing и cracking</a></p>
""",
            },
            "pa_context": {
                "title": "Пенсильвания, 2010 год",
                "content": """
<p>После переписи населения каждые 10 лет штаты перекраивают границы округов.</p>
<p>В 2010 году <span style=\"color:{REP_COLOR}\"><strong>республиканцы</strong></span>
выиграли выборы в законодательное собрание Пенсильвании — и получили право
рисовать карту 18 конгрессменов на следующие 10 лет.</p>
<p>Они воспользовались этим шансом по полной.</p>
<p style=\"margin-top: 1rem; font-size: 0.8em; color: #888;\">
Источник: <a href=\"https://en.wikipedia.org/wiki/Redistricting_in_Pennsylvania\" target=\"_blank\" style=\"color:#888;\">Redistricting in Pennsylvania</a></p>
""",
            },
            "map_2016": {
                "title": "Карта 2011 года — результаты выборов 2016",
                "content": """
<p>Вот карта, которую нарисовали республиканцы. Каждый округ закрашен по цвету
победившей партии:</p>
<p><span style=\"color:{DEM_COLOR}\">■</span> демократы &nbsp;
<span style=\"color:{REP_COLOR}\">■</span> республиканцы</p>
<p>Обратите внимание на <strong>причудливые формы</strong> округов —
они нарисованы не для удобства жителей, а для максимального
политического преимущества.</p>
""",
            },
            "goofy": {
                "title": "«Гуфи пинает Дональда Дака» — округ №7",
                "content": """
<p>Округ 7 стал символом этого безумия. Washington Post провёл конкурс на лучшее
название его формы — победило: <strong>«Гуфи пинает Дональда Дака»</strong>.</p>
<p>Округ растянулся на 80 км через пять каунти. В самом узком месте
его можно было пересечь буквально за полминуты: Усэйн Болт пробежал бы его очень быстро.</p>
<p>Зачем? Чтобы включить нужные предместья Филадельфии с республиканскими
избирателями и обойти демократические анклавы.</p>
<p>Результат: <span style=\"color:{REP_COLOR}\"><strong>республиканец победил
59% против 40%</strong></span>.</p>
<p style=\"margin-top: 1rem; font-size: 0.8em; color: #888;\">
Источники: <a href=\"https://www.washingtonpost.com/blogs/the-fix/post/name-that-district-contest-winner-goofy-kicking-donald-duck/2011/12/29/gIQA2Fa2OP_blog.html\" target=\"_blank\" style=\"color:#888;\">Washington Post</a>,
<a href=\"https://en.wikipedia.org/wiki/Pennsylvania%27s_7th_congressional_district\" target=\"_blank\" style=\"color:#888;\">PA-7 district</a></p>
""",
            },
            "packing": {
                "title": "Packing: демократы упакованы",
                "content": """
<p>Посмотрите на <span style=\"color:{DEM_COLOR}\"><strong>синие округа</strong></span>
вокруг Филадельфии — округа 1, 2 и 13.</p>
<p>Демократы здесь побеждают с гигантскими отрывами:</p>
<ul>
<li>Округ 1: <strong>82%</strong></li>
<li>Округ 2: <strong>90%</strong></li>
<li>Округ 13: <strong>100%</strong> (без соперника!)</li>
</ul>
<p>Все эти голоса «сгорают» — для победы достаточно 50%, но у демократов
по 80–100%. Это и есть <strong>packing</strong>.</p>
<p style=\"margin-top: 1rem; font-size: 0.8em; color: #888;\">
Источник: <a href=\"https://en.wikipedia.org/wiki/2016_United_States_House_of_Representatives_elections_in_Pennsylvania\" target=\"_blank\" style=\"color:#888;\">PA elections 2016</a></p>
""",
            },
            "cracking": {
                "title": "Cracking: пригороды раздроблены",
                "content": """
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
<p style=\"margin-top: 1rem; font-size: 0.8em; color: #888;\">
Источник: <a href=\"https://en.wikipedia.org/wiki/2016_United_States_House_of_Representatives_elections_in_Pennsylvania\" target=\"_blank\" style=\"color:#888;\">PA elections 2016</a></p>
""",
            },
            "results_2016": {
                "title": "Итог 2016: 45% голосов → 28% мест",
                "content": """
<p>Если считать <strong>фактические голоса по всему штату</strong> (сумма голосов во всех 18 округах),
пропорция была такой:</p>
<p><span style=\"color:{DEM_COLOR}\"><strong>Демократы: 45.7% голосов →
5 мест из 18 (28%)</strong></span></p>
<p><span style=\"color:{REP_COLOR}\"><strong>Республиканцы: 53.9% голосов →
13 мест из 18 (72%)</strong></span></p>
<p>Разрыв между долей голосов и долей мест — визитная карточка
джерримендеринга. Система работала идеально — для тех,
кто её нарисовал.</p>
<p style=\"margin-top: 1rem; font-size: 0.8em; color: #888;\">
Источник: <a href=\"https://en.wikipedia.org/wiki/2016_United_States_House_of_Representatives_elections_in_Pennsylvania\" target=\"_blank\" style=\"color:#888;\">PA elections 2016</a></p>
""",
            },
            "court": {
                "title": "Суд: карта неконституционна",
                "content": """
<p>В январе 2018 года <strong>Верховный суд Пенсильвании</strong> признал
карту 2011 года неконституционной.</p>
<p>Дело: <em>League of Women Voters v. Commonwealth of Pennsylvania</em>.</p>
<p>Суд постановил: карта нарушает Статью I Конституции штата
о свободных и честных выборах.</p>
<p>Республиканское законодательное собрание не смогло согласовать новую карту
до дедлайна, установленного судом.
Тогда <strong>суд нарисовал карту сам</strong>.</p>
<p style=\"margin-top: 1rem; font-size: 0.8em; color: #888;\">
Источник: <a href=\"https://en.wikipedia.org/wiki/League_of_Women_Voters_of_Pennsylvania_v._Commonwealth_of_Pennsylvania\" target=\"_blank\" style=\"color:#888;\">League of Women Voters v. Commonwealth of Pennsylvania</a></p>
""",
            },
            "map_2018": {
                "title": "Новая карта 2018 года",
                "content": """
<p>Вот карта, нарисованная судом. Сравните с предыдущей:</p>
<p>Округа стали <strong>компактными</strong> и <strong>географически
логичными</strong>. Никаких «Гуфи» — чёткие границы, следующие
границам каунти.</p>
<p><span style=\"color:{DEM_COLOR}\">■</span> демократы &nbsp;
<span style=\"color:{REP_COLOR}\">■</span> республиканцы</p>
<p style=\"margin-top: 1rem; font-size: 0.8em; color: #888;\">
Источник: <a href=\"https://en.wikipedia.org/wiki/League_of_Women_Voters_of_Pennsylvania_v._Commonwealth_of_Pennsylvania\" target=\"_blank\" style=\"color:#888;\">решение Верховного суда PA (2018)</a></p>
""",
            },
            "new_d7": {
                "title": "Что стало с «Гуфи»-территорией",
                "content": """
<p>После решения суда территорию старого «Гуфи»-округа в основном
разделили между новыми округами <strong>5</strong> и <strong>6</strong>
(частично — 4).</p>
<p>Результаты 2018: <span style=\"color:{DEM_COLOR}\"><strong>округ 5 — 65%</strong></span>,
<span style=\"color:{DEM_COLOR}\"><strong>округ 6 — 59%</strong></span> за демократов.</p>
<p>Когда границы становятся компактнее и логичнее, карта меньше искажает
реальную политическую географию региона.</p>
<p style=\"margin-top: 1rem; font-size: 0.8em; color: #888;\">
Источники: <a href=\"https://en.wikipedia.org/wiki/Pennsylvania%27s_7th_congressional_district\" target=\"_blank\" style=\"color:#888;\">история старого PA-7</a>,
<a href=\"https://en.wikipedia.org/wiki/2018_United_States_House_of_Representatives_elections_in_Pennsylvania\" target=\"_blank\" style=\"color:#888;\">PA elections 2018</a></p>
""",
            },
            "results_2018": {
                "title": "Итог 2018: справедливое представительство",
                "content": """
<p>Результат 2018 года:</p>
<p><span style=\"color:{DEM_COLOR}\"><strong>Демократы: 54.9% голосов →
9 мест из 18 (50%)</strong></span></p>
<p><span style=\"color:{REP_COLOR}\"><strong>Республиканцы: 44.7% голосов →
9 мест из 18 (50%)</strong></span></p>
<p>Представительство стало заметно справедливее: разрыв между долей голосов
и долей мест резко сократился по сравнению с 2016 годом.</p>
<p style=\"margin-top: 1rem; font-size: 0.8em; color: #888;\">
Источник: <a href=\"https://en.wikipedia.org/wiki/2018_United_States_House_of_Representatives_elections_in_Pennsylvania\" target=\"_blank\" style=\"color:#888;\">PA elections 2018</a></p>
""",
            },
            "conclusion": {
                "title": "Те же люди — другая карта",
                "content": """
<p><strong>Карта — не нейтральный инструмент.</strong> В 2016 году она превращала
45.7% голосов демократов в 28% мест. После судебной реформы карты
искажение стало значительно меньше.</p>
<p>Джерримендеринг — это когда выбирают не избиратели политиков,
а политики — своих избирателей.</p>
<p style=\"margin-top: 1.5rem; font-size: 0.85em; color: #888;\">
Источники:
<a href=\"https://en.wikipedia.org/wiki/League_of_Women_Voters_of_Pennsylvania_v._Commonwealth_of_Pennsylvania\" target=\"_blank\" style=\"color:#888;\">LWV v. Commonwealth of Pennsylvania (2018)</a>,
<a href=\"https://www.census.gov/\" target=\"_blank\" style=\"color:#888;\">US Census Bureau</a>,
<a href=\"https://en.wikipedia.org/wiki/2016_United_States_House_of_Representatives_elections_in_Pennsylvania\" target=\"_blank\" style=\"color:#888;\">PA elections 2016</a></p>
""",
            },
        },
        "grid": {
            "voters": "избирателей",
            "blue_pct": "синих",
            "red_pct": "красных",
            "fair_division": "Честное деление",
            "gerrymandering": "Джерримендеринг",
            "blue_count": "синих",
            "red_count": "красных",
            "minority_wins": "Меньшинство побеждает!",
            "same_people": "Те же 50 человек, те же линии",
            "votes_by_district": "Голоса по округам:",
            "district_prefix": "Округ",
        },
    },
}


def get_texts(locale: str) -> dict:
    """Return localized texts for a locale with BCP47-aware fallback to English."""
    if not locale:
        return TEXTS["en"]

    normalized = locale.replace("_", "-").lower()
    base = normalized.split("-", 1)[0]

    if normalized in TEXTS:
        return TEXTS[normalized]
    if base in TEXTS:
        return TEXTS[base]
    return TEXTS["en"]


def format_scene_content(template: str, *, dem_color: str, rep_color: str) -> str:
    """Format scene HTML template with party colors."""
    return template.format(DEM_COLOR=dem_color, REP_COLOR=rep_color)

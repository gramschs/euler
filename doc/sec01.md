---
jupytext:
  cell_metadata_filter: -all
  formats: md:myst
  main_language: python
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.7
---

# Das Euler-Verfahren

TODO

```{admonition} Lernziele
:class: goals
* Sie können eine gewöhnliche Differentialgleichung 1. Ordnung mit Anfangswert
  mit dem **Euler-Verfahren** numerisch lösen.
* Sie können das Euler-Verfahren in Python implementieren.
* Sie kennen den Einfluss der **Schrittweite** auf den Fehler des
  Euler-Verfahrens.
* Sie können mit **solve_ivp()** aus dem Modul `scipy.integrate` ein
  Anfangswertproblem lösen.
```

## Geschwindigkeit aus der Beschleunigung rekonstruieren

Wir führen das folgenden Experiment aus. Eine Person setzt sich auf ein Bobby
Car und fährt eine kurze Zeit, so schnell sie kann.

```{figure} pics/bobby_car_symbolbild.jpg
---
width: 50%
name: fig01
---
Symbolbild der Bobby-Car-Fahrt
(Quelle: [Freepik](https://www.freepik.com/premium-photo/side-view-cute-girl-sitting-toy-car-outdoors_106394881.htm#fromView=search&page=4&position=34&uuid=addb4ac3-8613-4e05-9193-09f3127bd114&query=Bobby+car), Lizenz: Freepik Premium Lizenz)
```

Zu Beginn der Bobby-Car-Fahrt ist die Geschwindigkeit Null. Wir bezeichnen die
Geschwindigkeit mit $v$ \[m/s\] und die Zeit mit $t$ \[s\].
Es gilt also für den Start $t_0 = 0 \,\mathrm{s}$

$$v(0) = 0 \frac{\mathrm{m}}{\mathrm{s}}.$$

Die Beschleunigung messen wir mit Hilfe eines Smartphones und der App
[Phyphox](https://phyphox.org). Beispielhaft erhalten wir die folgenden
Beschleunigungsmessungen, die wir mit dem Python-Modul Pandas importieren.

```{code-cell}
import pandas as pd

daten = pd.read_excel('data/Beschleunigung_V01.xls')
daten.info()
```

Wir verwenden das Python-Modul Plotly, um die Beschleunigungsdaten in x-Richtung
abhängig von der Zeit zu visualisieren. Die x-Richtung wird gewählt, weil das
Smartphone beim Experiment entsprechend montiert war (siehe [Koordinatensystem
von Phyphox](https://phyphox.org/de/unterstutzte-sensoren/)).

```{code-cell}
import plotly.express as px

fig = px.scatter(daten, x = 'Time (s)', y = 'Linear Acceleration x (m/s^2)')
fig.show()
```

Damit wir einfacher auf die Messdaten zugreifen können, speichern wir die
Zeitmessungen `Time (s)` in der Variablen `t` und die Beschleunigung `Linear
Acceleration x (m/s^2)` in der Variablen `a`.

```{code-cell}
t = daten['Time (s)']
a = daten['Linear Acceleration x (m/s^2)']
```

Nun wollen wir numerisch die Geschwindigkeiten aus den Beschleunigungsdaten
rekonstruieren. Generell führt eine konstante Beschleunigung $a$, die eine
Zeitdauer $\Delta t$ lang wirkt, zu einer Geschwindigkeitsänderung $\Delta v$:

$$\Delta v = a \cdot \Delta t.$$

Da wir nur diskrete Messwerte vorliegen haben, nehmen wir an, dass die
Beschleunigung $a_0$ konstant im Zeitintervall $[t_0, t_1]$ gewirkt hat und
können damit nun die neue Geschwindigkeit $v_1$ berechnen. In mathematischen
Formeln erhalten wir

$$v_1 - v_0 = a_0 \cdot (t_1 - t_0)\quad
\Rightarrow \quad v_1 = v_0 + a_0 \cdot (t_1 - t_0).$$

In Python ergibt sich mit dem Anfangswert `v0 = 0`

```{code-cell}
# Anfangswert
t0 = 0
v0 = 0

# neue Geschwindigkeit
v1 = v0 + a[0] * (t[1] - t0)
print(f'v1 = {v1}')
```

Jetzt, wo wir $v_1$ berechnet haben, können wir erneut annehmen, dass $a_1$
konstant im Zeitintervall $[t_1, t_2]$ gewirkt hat und erhalten:

$$v_2 - v_1 = a_1 \cdot (t_2 - t_1)\quad
\Rightarrow \quad v_2 = v_1 + a_1 \cdot (t_2 - t_1).$$

In Python ergibt sich

```{code-cell}
v2 = v1 + a[1] * (t[2] - t[1])
print(f'v2 = {v2}')
```

Diese Prozedur können wir immer weiter fortsetzen, bis wir die Geschwindigkeit
auf dem gesamten gemessenen Zeitintervall rekonstruiert haben. Es ist einfacher,
Python die Arbeit machen zu lassen. Daher bestimmen wir zunächst die Anzahl der
Messwerte $N$ und initialisieren anschließend ein NumPy-Array der Länge $N$, das
die Geschwindigkeitswerte aufnehmen soll.

```{code-cell}
import numpy as np

N = len(t)
v = np.zeros(N)
```

Die obige Berechnung der Geschwindigkeitsänderung

$$\Delta v = a \cdot \Delta t$$

lässt sich für beliebige Zeitintervalle $[t_i, t_{i+1}]$ formulieren als

$$v_{i+1} - v_{i} = a_{i} \cdot (t_{i+1} - t_{i})\quad
\Rightarrow \quad v_{i+1} = v_{i} + a_{i} \cdot (t_{i+1} - t_{i}).$$

Danach können wir von Python die Berechnung der Geschwindigkeitswerte mit einer
Schleife durchführen lassen:

```{code-cell}
for i in range(1, N-1):
    v[i+1] = v[i] + a[i] * (t[i+1] - t[i])
```

Nun können wir die berechneten Geschwindigkeiten visualisieren.

```{code-cell}
fig = px.line(x = t, y = v,
  labels = {'x': 'Time (s)', 'y': 'Velocity in x (m/s)'})
fig.show()
```

## Anfangswertprobleme allgemein mit dem Euler-Verfahren lösen

In dem obigen Beispiel haben wir aus der Messung einer Beschleunigung die
Geschwindigkeit rekonstruiert. Allgemein betrachtet kann der Zusammenhang
zwischen Geschwindigkeit und Beschleunigung über die Differentialgleichung

$$\dot{v}(t) = a(t)$$

beschrieben werden. Es liegt eine **Differentialgleichung 1. Ordnung** vor.
Zusammen mit der Forderung, dass zu einem reellen Startwert $t_0$ die
Geschwindigkeit gleich dem  Anfangswert $v_0$ ist, also

$$v(t_0) = v_0$$

gilt, stellt das Bobby-Car-Problem ein **Anfangswertproblem** dar. Wir können
die oben beschriebene Prozedur auf beliebige Anfangswertprobleme übertragen,
indem wir selbst das zu untersuchende Intervall in Zeitpunkte unterteilen.

Wenn das allgemeine Anfangswertproblem

$$\dot{x}(t) = f(t, x(t)), \; x(t_0) = x_0$$

lautet, dann beginnen wir beim Anfangswert $t_0$ und nutzen die Schrittweite 
$h > 0$, um Zeitpunkte

$$t_{i} = t_0 + i\cdot h, \quad i = 0, 1, 2, \ldots$$

zu erzeugen. Dann wird die Lösungsfunktion $x$ durch die Punkte

$$x_{i+1} = x_{i} + f(t_{i}, x_{i}) \cdot h, \quad i = 0, 1, 2, \ldots$$

angenähert. Dabei haben wir die Abkürzung $x_{i}$ für $x_{i} = x(t_{i})$
verwendet. Wir hangeln uns also immer ein Stückchen "h" weiter.

## Abbremsen eines Bobby-Cars

Um dieses Verfahren zu
erläutern, betrachten wir ein weiteres Beispiel. Angenommen, dass Bobby-Car hat
zum Zeitpunkt $t_0 = 0 \mathrm{s}$ die Geschwindigkeit $v_0 = 41
\frac{\mathrm{m}}{\mathrm{s}}$. Der Fahrer entscheidet sich, das Bobby-Car
ausrollen zu lassen. Es wirken eine lineare Bremskraft und die Luftreibung, was
sich als nichtlineare Differentialgleichung 1. Ordnung formulieren lässt:

$$\dot{v}(t) = -\alpha - \beta v(t)^2.$$

Wir möchten den Geschwindigkeitsverlauf für das Intervall $[0, 30 \mathrm{s}]$
numerisch mit dem Euler-Verfahren ermitteln. Wir wählen als sogenannte
Schrittweite

$$h = 1 \mathrm{s}$$

und brauchen daher 31 Zeitpunkte. Dann gilt

$$v_{i+1} = v_{i} + (-\alpha - \beta v_{i}^2))$$

```{code-cell}
t = np.zeros(N)
v = np.zeros(N)

for i in range(1, N-1):
  pass
```

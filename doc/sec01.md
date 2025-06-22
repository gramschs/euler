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

Das Euler-Verfahren ist das einfachste numerische Verfahren zur Lösung eines
Anfangswertproblems. Zum Verständnis benötigen wir Vorkenntnisse über

* Differentialgleichungen 1. Ordnung,
* Taylorpolynom Grad 1 und
* Python-Kenntnisse (Pandas, for-Schleife, Plotly).

## Lernziele

```{admonition} Lernziele
:class: goals
* Sie können eine Bewegung als Anfangswertproblem formulieren.
* Sie können das **Euler-Verfahren** zur numerischen Lösung eines
  Anfangswertproblems in Python implementieren.
* Sie können mit der Tangente bzw. dem Taylorpolynom 1. Grades begründen, warum
  das Euler-Verfahren funktioniert.
* Sie wissen, welchen Einfluss die **Schrittweite** auf den Fehler des
  Euler-Verfahrens hat.
```

## Geschwindigkeit aus der Beschleunigung rekonstruieren

Wir führen das folgende Experiment aus. Eine Person setzt sich auf ein Bobby
Car und fährt eine kurze Zeit, so schnell sie kann.

```{figure} pics/bobby_car_symbolbild.jpg
---
width: 50%
name: fig01
class: responsive-image
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

daten = pd.read_csv('data/Beschleunigung.csv')
daten.info()
```

Mit der Methode `.head()` lassen wir uns die ersten 10 Zeilen der importierten
Tabelle anzeigen:

```{code-cell}
daten.head(10)
```

Wir verwenden das Python-Modul Plotly Express, um die Beschleunigungsdaten in
x-Richtung abhängig von der Zeit zu visualisieren. Die x-Richtung wird gewählt,
weil das Smartphone beim Experiment entsprechend montiert war (siehe
[Koordinatensystem von Phyphox](https://phyphox.org/de/unterstutzte-sensoren/)).

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

In Python ergibt sich mit dem Anfangswert `v0 = 0`:

```{code-cell}
# Anfangswert für t[0]
v0 = 0

# neue Geschwindigkeit
v1 = v0 + a[0] * (t[1] - t[0])
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
auf dem gesamten gemessenen Zeitintervall rekonstruiert haben. Das wollen wir
nicht händisch, sondern automatisiert mit Python machen. Daher bestimmen wir
zunächst die Anzahl der Messwerte $N$ und initialisieren anschließend ein
NumPy-Array der Länge $N$, das die Geschwindigkeitswerte aufnehmen soll.

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

Wird eine for-Schleife verwendet, berechnet der folgende Python-Code
nacheinander die Geschwindigkeitswerte aus den diskreten
Beschleunigungsmessungen:

```{code-cell}
for i in range(N-1):
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
Geschwindigkeit gleich der Anfangsgeschwindigkeit $v_0$ ist, also

$$v(t_0) = v_0$$

gilt, stellt das Bobby-Car-Problem ein **Anfangswertproblem** dar. Wir können
die oben beschriebene Prozedur auf beliebige Anfangswertprobleme übertragen.

```{admonition} Euler-Verfahren
:class: note
Wenn das allgemeine Anfangswertproblem

$$\dot{x}(t) = f(t, x(t)), \quad x(t_0) = x_0$$

lautet, dann beginnen wir beim Anfangswert $t_0$ und nutzen die **Schrittweite**
$h > 0$, um Punkte

$$t_{i} = t_0 + i\cdot h, \quad i = 0, 1, 2, \ldots$$

zu erzeugen. Diese Punkte werden als **Gitter** bezeichnet. Dann wird die
Lösungsfunktion $x$ durch die Werte

$$x_{i+1} = x_{i} + f(t_{i}, x_{i}) \cdot h, \quad i = 0, 1, 2, \ldots$$

angenähert. Dabei haben wir die Abkürzung $x_{i}$ für $x_{i} = x(t_{i})$
verwendet. Wir hangeln uns also immer ein Stückchen "h" weiter. Diese Prozedur
wird **Euler-Verfahren** genannt.
```

Begründen lässt sich das Euler-Verfahren mit der Taylor-Formel bzw. der
Tangentengleichung. Das Taylorpolynom vom Grad 1 an einem Entwicklungspunkt
$t_{*}$ lautet

$$T_{1, f}(t) = f(t_{*}) + f'(t_{*})\cdot (t-t_{*}).$$

Übertragen auf unser Anfangswertproblem lautet das Taylorpolynom vom Grad 1 für
den Entwicklungspunkt $t_i$

$$T_{1,x}(t) = x(t_{i}) + \dot{x}(t_{i}) \cdot (t-t_{i}).$$

Wir gehen davon aus, dass wir in der Nähe des Entwicklungspunktes das
Taylorpolynom als Ersatz für die exakte Lösungsfunktion nehmen dürfen und
setzen für die erste Ableitung $\dot{x}$ die rechte Seite $f(t_i, x(t_i))$ der
Differentialgleichung ein.

```{figure} pics/tangente.pdf
---
name: tangente
class: responsive-image
width: 80%
---
Tangente bzw. Taylorpolynom 1. Grades für die Lösungsfunktion des
Anfangswertproblems $\dot{x}(t) = -0.003 x(t)^2, \; x(0)=5$ (Quelle: eigene
Darstellung, Lizenz: BY-NC-SA-4.0)
```

Damit erhalten wir

$$x(t) = x(t_{i}) + f(t_{i}, x(t_i)) \cdot (t-t_{i}).$$

Speziell für den nächsten Gitterpunkt $t_{i+1}$ gilt dann näherungsweise

$$x(t_{i+1}) = x(t_{i}) + f(t_{i}, x(t_i)) \cdot (t_{i+1}-t_{i}),$$

was mit den Abkürzungen $x_i=x(t_i)$ und $x_{i+1} = x(t_{i+1})$ vereinfacht
geschrieben werden kann als

$$x_{i+1} = x_{i} + f(t_{i}, x_i) \cdot h.$$

Wenn wir für $t_i$ den Wert der Lösungsfunktion $x_i$ kennen würden, könnten wir
damit für den nächsten Punkt $t_{i+1}$ den Wert $x_{i+1}$ berechnen. Da wir ein
Anfangswertproblem vorliegen haben, kennen wir $t_0$ und $x_0$ und können so auf
$t_1$ und $x_1$ schließen. Und damit wiederum können wir $t_2$ und $x_2$
berechnen und so weiter, bis wir schließlich eine angenäherte Lösungsfunktion
auf dem kompletten Intervall gefunden haben.

Das Euler-Verfahren ist das einfachste numerische Verfahren zur Lösung eines
Anfangswertproblems. Es hat aber auch Nachteile und lässt sich nicht immer
stabil einsetzen. Im nächsten Abschnitt erkunden wir, welchen Einfluss die
Schrittweite $h$ auf die Qualität der angenäherten Lösung hat.

```{dropdown} Video "Euler Verfahren" von Kochrezepte für Mathematik
<iframe width="560" height="315" src="https://www.youtube.com/embed/EhyNxBeNZuM?si=-7IA3p8mIU4aHDeC" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

## Einfluss der Schrittweite

Wie gut die numerische Lösung eine exakte Lösung eines Anfangswertproblems
annähert, wird auch durch die Schrittweite bestimmt. Um den Zusammenhang
zwischen der Schrittweite $h$ und den Fehler des Euler-Verfahrens zu verstehen,
betrachten wir das folgende Beispiel.

Ein Bobby-Car fährt mit einer Anfangsgeschwindigkeit von $v_0 = 5
\mathrm{m}/\mathrm{s}$. Der Fahrer oder die Fahrerin lässt das Bobby-Car
ausrollen. Dann gilt für das Abbremsen des Bobby-Cars die folgende
Differentialgleichung

$$\dot{v}(t) = - k \cdot v(t)^2,$$

wobei wir annehmen, dass der Abbremsvorgang zum Zeitpunkt $t = 0\,\mathrm{s}$
beginnt. Die Konstante $k$ ergibt sich aus dem Luftwiderstand und hat in unserem
Fall einen Wert von

$$k = 0.003 \frac{1}{\mathrm{m}}.$$

Als nächstes variieren wir die Schrittweite $h>0$.

```{admonition} Mini-Übung
:class: miniexercise, dropdown
Öffnen Sie im Browser die interaktive Demonstration des Euler-Verfahrens

[https://gramschs.github.io/euler/_static/assets/interactive_euler_demo.html](https://gramschs.github.io/euler/_static/assets/interactive_euler_demo.html)

für die Abbremsung des Bobby-Cars. Variieren Sie die Schrittweite h und
beobachten Sie, wie gut oder schlecht die Annäherung an die exakte Lösung ist.
Legen Sie eine Tabelle an:

| Schrittweite h    | relativer Endfehler in Prozent |
| ------------- | ------------- |
| 1 | ? |
| 5 | ? |
| ... | ??? |

Stellen Sie eine Vermutung an. Wie hängt der Endfehler von der Schrittweite ab?
```

```{admonition} Lösung
:class: minisolution, toggle
Es gibt mehrere Fehlerarten. Wir betrachten hier den relativen Endfehler in
Prozent.

| Schrittweite h    | relativer Endfehler in Prozent  |
| ------------- | ------------- |
| 1   | 0.47  |
| 5   | 2.35  |
| 10  | 4.74  |
| 15  | 7.20  |
| 20  | 9.74  |
| 25  | 12.41 |
| 30  | 15.30 |
| 35  | 19.05 |
| 40  | 23.03 |
| 45  | 28.54 |
| 50  | 34.11 |

Vermutung: für große Schrittweiten $h$ hängt der relative Endfehler linear von
der Schrittweite ab.
```

Wir können verschiedene Arten von Fehler in Abhängigkeit von der Schrittweite
untersuchen, beispielsweise

* maximaler Fehler,
* Gesamtfehler (RMSE) und
* relativer Endfehler (in Prozent).

Für den maximalen Fehler wird für jeden Gitterpunkt der Abstand zwischen der
angenäherten und der exakten Lösung berechnet. Der größte Abstand wird dann als
maximaler Fehler bezeichnet. Beim Gesamtfehler wird die Wurzel aus dem mittleren
quadratischen Fehler betrachtet, was auch als [Root Mean Square
Error](https://statorials.org/de/wie-man-rmse-interpretiert/) bezeichnet wird.
Beim relativen Endfehler wird nur der letzte Gitterpunkt betrachtet und der
Abstand zum exakten Funktionswert in Prozent angegeben.

In dem folgenden Streudiagramm ist der relative Endfehler in Prozent für
verschiedene Schrittweiten dargestellt. Er summiert sich über alle
Iterationen auf und wird daher auch als globaler Fehler bezeichnet. Beim
Euler-Verfahren hängt er linear von der Schrittweite ab.

```{code-cell}
:tags: [remove-input]
import numpy as np

# data
h = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
rmse_fehler = [0.0091, 0.0467, 0.0967, 0.1511, 0.2113, 0.2790, 0.3561, 0.4568, 0.5617, 0.6923, 0.8024]
endfehler_in_prozent = [0.47, 2.35, 4.74, 7.2, 9.74, 12.41, 15.3, 19.05, 23.03, 28.54, 34.11]

# regression
p = np.polyfit(h, endfehler_in_prozent, 1)
x_model = np.linspace(0, 50, 101)
y_model = np.polyval(p, x_model)

# plot
fig = px.scatter(x = h, y = endfehler_in_prozent,
  title='Endfehler abhängig von Schrittweite h',
  labels={'x': 'Schrittweite h', 'y': 'relativer Endfehler in Prozent'})
fig.add_scatter(x = x_model, y = y_model, mode='lines', name='Regression')
fig.show()
```

Wir können auch andere Fehler betrachten. Der Fehler, der von einer zu nächsten
Iteration entsteht, wird beispielsweise als lokaler Fehler bezeichnet. Beim
Euler-Verfahren ist der lokale Fehler quadratisch abhängig von der Schrittweite.

## Zusammenfassung und Ausblick

Das Euler-Verfahren ist ein sehr einfaches Verfahren zur numerischen Lösung
eines Anfangswertproblems. Es kann verbessert werden, wenn nicht eine feste,
sondern eine variable Schrittweite gewählt wird (Schrittweitensteuerung).
Weitere Varianten des Euler-Verfahrens sind das implizite Euler-Verfahren und
das Euler-Maruyama-Verfahren für stochastische Differentialgleichungen.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def euler_integration_velocity(time_data, acceleration_data, initial_velocity=0.0):
    """
    Rekonstruiert die Geschwindigkeit aus Beschleunigungsdaten mit dem Euler-Verfahren.
    
    Parameter:
    - time_data: Array mit Zeitwerten [s]
    - acceleration_data: Array mit Beschleunigungswerten [m/s²]
    - initial_velocity: Anfangsgeschwindigkeit [m/s] (Standard: 0.0)
    
    Returns:
    - velocity_data: Array mit Geschwindigkeitswerten [m/s]
    """
    
    # Initialisierung
    velocity = np.zeros(len(time_data))
    velocity[0] = initial_velocity
    
    # Euler-Integration: v(t+dt) = v(t) + a(t) * dt
    for i in range(1, len(time_data)):
        dt = time_data[i] - time_data[i-1]  # Zeitschritt
        velocity[i] = velocity[i-1] + acceleration_data[i-1] * dt
    
    return velocity

def load_and_process_data(filename):
    """
    Lädt Excel-Datei und extrahiert Zeit- und Beschleunigungsdaten.
    """
    
    # Excel-Datei laden
    df = pd.read_excel(filename, sheet_name='Raw Data')
    
    # Daten extrahieren
    time_data = df['Time (s)'].values
    accel_x_data = df['Linear Acceleration x (m/s^2)'].values
    
    return time_data, accel_x_data

def plot_results(time_data, accel_data, velocity_data):
    """
    Erstellt Diagramme für Beschleunigung und rekonstruierte Geschwindigkeit.
    """
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Beschleunigung plotten
    ax1.plot(time_data, accel_data, 'b-', linewidth=1, label='Beschleunigung x')
    ax1.set_xlabel('Zeit [s]')
    ax1.set_ylabel('Beschleunigung [m/s²]')
    ax1.set_title('Gemessene Beschleunigung in x-Richtung')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Geschwindigkeit plotten
    ax2.plot(time_data, velocity_data, 'r-', linewidth=1, label='Geschwindigkeit x')
    ax2.set_xlabel('Zeit [s]')
    ax2.set_ylabel('Geschwindigkeit [m/s]')
    ax2.set_title('Rekonstruierte Geschwindigkeit in x-Richtung (Euler-Verfahren)')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.show()

def main():
    """
    Hauptprogramm: Lädt Daten, führt Integration durch und zeigt Ergebnisse.
    """
    
    # Datei laden (passen Sie den Pfad an!)
    filename = 'Beschleunigung_V01.xls'
    
    try:
        # Daten laden
        time_data, accel_x_data = load_and_process_data(filename)
        
        print(f"Daten geladen:")
        print(f"- Anzahl Messpunkte: {len(time_data)}")
        print(f"- Zeitbereich: {time_data[0]:.3f}s bis {time_data[-1]:.3f}s")
        print(f"- Beschleunigungsbereich: {np.min(accel_x_data):.3f} bis {np.max(accel_x_data):.3f} m/s²")
        
        # Geschwindigkeit mit Euler-Verfahren rekonstruieren
        velocity_data = euler_integration_velocity(time_data, accel_x_data, initial_velocity=0.0)
        
        print(f"\nGeschwindigkeit rekonstruiert:")
        print(f"- Geschwindigkeitsbereich: {np.min(velocity_data):.3f} bis {np.max(velocity_data):.3f} m/s")
        print(f"- Endgeschwindigkeit: {velocity_data[-1]:.3f} m/s")
        
        # Ergebnisse plotten
        plot_results(time_data, accel_x_data, velocity_data)
        
        # Optional: Ergebnisse in CSV speichern
        results_df = pd.DataFrame({
            'Time_s': time_data,
            'Acceleration_x_ms2': accel_x_data,
            'Velocity_x_ms': velocity_data
        })
        
        results_df.to_csv('velocity_reconstruction_results.csv', index=False)
        print("\nErgebnisse gespeichert in: velocity_reconstruction_results.csv")
        
        return time_data, accel_x_data, velocity_data
        
    except FileNotFoundError:
        print(f"Fehler: Datei '{filename}' nicht gefunden!")
        print("Stellen Sie sicher, dass die Excel-Datei im gleichen Verzeichnis liegt.")
        return None, None, None
    
    except Exception as e:
        print(f"Fehler beim Verarbeiten der Daten: {str(e)}")
        return None, None, None

# Erweiterte Analyse-Funktionen
def analyze_integration_quality(time_data, velocity_data):
    """
    Analysiert die Qualität der numerischen Integration.
    """
    
    # Zeitschritt-Analyse
    dt_values = np.diff(time_data)
    dt_mean = np.mean(dt_values)
    dt_std = np.std(dt_values)
    
    print(f"\nIntegrations-Qualitätsanalyse:")
    print(f"- Mittlerer Zeitschritt: {dt_mean*1000:.2f} ms")
    print(f"- Zeitschritt-Standardabweichung: {dt_std*1000:.2f} ms")
    print(f"- Zeitschritt-Variabilität: {(dt_std/dt_mean)*100:.2f}%")
    
    # Drift-Analyse (sollte bei ruhendem Objekt gegen 0 gehen)
    final_velocity = velocity_data[-1]
    print(f"- Geschwindigkeits-Drift: {final_velocity:.3f} m/s")
    
    if abs(final_velocity) > 0.1:
        print("  ⚠️  Warnung: Große Geschwindigkeits-Drift erkannt!")
        print("     Dies könnte auf Sensor-Offset oder Integrationsfehler hindeuten.")

if __name__ == "__main__":
    # Programm ausführen
    time, accel, velocity = main()
    
    # Zusätzliche Analyse (falls Daten erfolgreich geladen)
    if time is not None:
        analyze_integration_quality(time, velocity)
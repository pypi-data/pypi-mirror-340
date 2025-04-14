import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from IPython.display import clear_output, display, HTML
import plotly.graph_objects as go
from google.colab import files
from scipy import ndimage, signal
from scipy.signal import savgol_filter
from scipy.signal import find_peaks
from scipy.integrate import quad
from scipy import integrate
import plotly.graph_objects as go
import os
import shutil
from io import BytesIO
from datetime import datetime
import openpyxl
from openpyxl.drawing.image import Image
from scipy.stats import norm

def DistribucionFOKVectorial(Im,E,Tm,Tabs):
  ## Variables Aproximacion racional de las segunda Integral Exponencial
  Kb = 8.617333262e-5  # eV/K
  a1 = 8.5733287401
  a2 = 18.059016973
  a3 = 8.6347608925
  a4 = 0.2677737343

  b1 = 9.5733223454
  b2 = 25.6329561486
  b3 = 21.0996530827
  b4 = 3.9584969228

  # Vectorizamoa
  alpha2_0=[]
  alpha1_0=[]
  xli=[]
  Xli2=[]
  Resultado=[]

  for i in range (len(Tabs)):

    x1_0 = (E / (Kb * Tm)) * ((E / (Kb * Tm)) * ((E / (Kb * Tm)) * ((E / (Kb * Tm)) + a1) + a2) + a3) + a4
    x2_0 = (E / (Kb * Tm)) * ((E / (Kb * Tm)) * ((E / (Kb * Tm)) * ((E / (Kb * Tm)) + b1) + b2) + b3) + b4
    alpha1_0.append(x1_0 / x2_0)


    x1_0 = (E / (Kb * Tabs[i])) * ((E / (Kb * Tabs[i])) * ((E / (Kb * Tabs[i])) * ((E / (Kb * Tabs[i])) + a1) + a2) + a3) + a4
    x2_0 = (E / (Kb * Tabs[i])) * ((E / (Kb * Tabs[i])) * ((E / (Kb * Tabs[i])) * ((E / (Kb * Tabs[i])) + b1) + b2) + b3) + b4
    alpha2_0.append(x1_0 / x2_0)

    xli.append(np.exp((E / (Kb * Tm)) - (E / (Kb * Tabs[i]))))

    Xli2.append(xli[len(xli)-1] * (Tabs[i] / Tm) * (1 - alpha2_0[len(alpha2_0)-1]))

    Xli2[len(Xli2)-1] = (1 - alpha1_0[len(alpha2_0)-1]) - Xli2[len(Xli2)-1]

    Xli2[len(Xli2)-1] = (E / (Kb * Tm)) * Xli2[len(Xli2)-1]

    Resultado.append(Im*xli[len(xli)-1] * np.exp(Xli2[len(Xli2)-1]))

  return Resultado

def DistribucionCTD_Exp (Im, E_0, Tm, sigma, Tabs):
    # Definir la constante de Boltzmann
    Kb = 8.617333262e-5  # eV/K
    # Variables Aproximacion racional de las segunda Integral Exponencial
    a1, a2, a3, a4 = 8.5733287401, 18.059016973, 8.6347608925, 0.2677737343
    b1, b2, b3, b4 = 9.5733223454, 25.6329561486, 21.0996530827, 3.9584969228

    E1 = E_0
    E2 = E_0 + 9 * sigma
    Resultado=[]
    Resultado_num = []
    Resultado_den = []

    for i in range (len(Tabs)):

        def integrand_num(E):
            #calculo de R(x) = 1 - alpha1_0
            x1_0 = (E / (Kb * Tabs[i])) * ((E / (Kb * Tabs[i])) * ((E / (Kb * Tabs[i])) * ((E / (Kb * Tabs[i])) + a1) + a2) + a3) + a4
            x2_0 = (E / (Kb * Tabs[i])) * ((E / (Kb * Tabs[i])) * ((E / (Kb * Tabs[i])) * ((E / (Kb * Tabs[i])) + b1) + b2) + b3) + b4
            alpha1_0 = (x1_0 / x2_0)

            # Gaussian distribution function
            fg_E = (1 / (np.sqrt (2 * np.pi) * sigma)) * np.exp(-(E - E_0)**2 / (2 * sigma**2))
            # Exponential distribution function
            fe_E=(1 / sigma) * np.exp(-(E - E_0) / (sigma))
            f_E = fe_E
            return f_E * np.exp(-E / (Kb * Tabs[i])) * np.exp(-(E_0/(Kb * Tm)) * (Tabs[i] / Tm) * np.exp((E_0 / (Kb*Tm)) - (E/( Kb * Tabs[i]))) * (1 - alpha1_0))
        resultado_num, _ = integrate.quad(integrand_num, E1, E2)
        Resultado_num.append(resultado_num)
        def integrand_den(E):
            #calculo de R(x) = 1 - alpha2_0
            x3_0 = (E / (Kb * Tm)) * ((E / (Kb * Tm)) * ((E / (Kb * Tm)) * ((E / (Kb * Tm)) + a1) + a2) + a3) + a4
            x4_0 = (E / (Kb * Tm)) * ((E / (Kb * Tm)) * ((E / (Kb * Tm)) * ((E / (Kb * Tm)) + b1) + b2) + b3) + b4
            alpha2_0 = x3_0 / x4_0
            # Gaussian distribution function
            fg_E = (1 / (np.sqrt (2 * np.pi) * sigma)) * np.exp(-(E - E_0)**2 / (2 * sigma**2))
            # Exponential distribution function
            fe_E=(1 / sigma) * np.exp(-(E - E_0) / (sigma))
            f_E = fe_E
            return f_E * np.exp(-E / (Kb * Tm)) * np.exp(-(E_0 / (Kb * Tm)) * np.exp((E_0 / (Kb * Tm)) - (E / (Kb * Tm))) * (1 - alpha2_0))
        resultado_den, _ = integrate.quad(integrand_den, E1, E2)
        Resultado_den.append(resultado_den)
        Resultado.append(Im * (resultado_num / resultado_den))
    return Resultado



def DistribucionCTD_Gaus (Im, E_0, Tm, sigma, Tabs):
    # Definir la constante de Boltzmann
    Kb = 8.617333262e-5  # eV/K
    # Variables Aproximacion racional de las segunda Integral Exponencial
    a1, a2, a3, a4 = 8.5733287401, 18.059016973, 8.6347608925, 0.2677737343
    b1, b2, b3, b4 = 9.5733223454, 25.6329561486, 21.0996530827, 3.9584969228

    E1 = E_0 - 3 * sigma
    E2 = E_0 + 3 * sigma
    Resultado=[]
    Resultado_num = []
    Resultado_den = []

    for i in range (len(Tabs)):

        def integrand_num(E):
            #calculo de R(x) = 1 - alpha1_0
            x1_0 = (E / (Kb * Tabs[i])) * ((E / (Kb * Tabs[i])) * ((E / (Kb * Tabs[i])) * ((E / (Kb * Tabs[i])) + a1) + a2) + a3) + a4
            x2_0 = (E / (Kb * Tabs[i])) * ((E / (Kb * Tabs[i])) * ((E / (Kb * Tabs[i])) * ((E / (Kb * Tabs[i])) + b1) + b2) + b3) + b4
            alpha1_0 = (x1_0 / x2_0)

            # Gaussian distribution function
            fg_E = (1 / (np.sqrt (2 * np.pi) * sigma)) * np.exp(-(E - E_0)**2 / (2 * sigma**2))
            # Exponential distribution function
            fe_E=(1 / sigma) * np.exp(-(E - E_0) / (sigma))
            f_E = fg_E
            return f_E * np.exp(-E / (Kb * Tabs[i])) * np.exp(-(E_0/(Kb * Tm)) * (Tabs[i] / Tm) * np.exp((E_0 / (Kb*Tm)) - (E/( Kb * Tabs[i]))) * (1 - alpha1_0))
        resultado_num, _ = integrate.quad(integrand_num, E1, E2)
        Resultado_num.append(resultado_num)
        def integrand_den(E):
            #calculo de R(x) = 1 - alpha2_0
            x3_0 = (E / (Kb * Tm)) * ((E / (Kb * Tm)) * ((E / (Kb * Tm)) * ((E / (Kb * Tm)) + a1) + a2) + a3) + a4
            x4_0 = (E / (Kb * Tm)) * ((E / (Kb * Tm)) * ((E / (Kb * Tm)) * ((E / (Kb * Tm)) + b1) + b2) + b3) + b4
            alpha2_0 = x3_0 / x4_0
            # Gaussian distribution function
            fg_E = (1 / (np.sqrt (2 * np.pi) * sigma)) * np.exp(-(E - E_0)**2 / (2 * sigma**2))
            # Exponential distribution function
            fe_E=(1 / sigma) * np.exp(-(E - E_0) / (sigma))
            f_E = fg_E
            return f_E * np.exp(-E / (Kb * Tm)) * np.exp(-(E_0 / (Kb * Tm)) * np.exp((E_0 / (Kb * Tm)) - (E / (Kb * Tm))) * (1 - alpha2_0))
        resultado_den, _ = integrate.quad(integrand_den, E1, E2)
        Resultado_den.append(resultado_den)
        Resultado.append(Im * (resultado_num / resultado_den))
    return Resultado

def PeakDetection(DatosEntrada, suavizado, distancia,Umbral):
  # Guardar la curva en variables
  tem_entrada = DatosEntrada.iloc[:, 0]  # Temperatura en °C
  Tabs_entrada = tem_entrada + 273.15  # Convertir a Kelvin
  intensidad_entrada = DatosEntrada.iloc[:, 1]  # Intensidad

    # Aplicar suavizado a la intensidad
  # -----------------------------------------------
  # window_length=11, polyorder=5  # Muy suavizado
  # window_length=9,  polyorder=4
  # window_length=7,  polyorder=3
  # window_length=5,  polyorder=3
  # window_length=3,  polyorder=2  # Mínimo suavizado
  # -----------------------------------------------
  match int(suavizado):
        case 0:
            wl=11
            po=5
        case 1:
            wl=9
            po=4
        case 2:
            wl=7
            po=3
        case 3:
            wl=5
            po=3
        case _:
            wl=3
            po=2

  intensidad_suavizada = savgol_filter(intensidad_entrada, window_length=int(wl), polyorder=int(po))
  dx=tem_entrada.iloc[1] - tem_entrada.iloc[0]
  dIntensidad_smoth = np.diff(np.diff(intensidad_suavizada)/dx)/dx
  dIntensidad_smoth=savgol_filter(dIntensidad_smoth,window_length=int(wl), polyorder=int(po))

  # Umbral de intensidad para descartar los picos
  umbral_intensidad = float(Umbral) * max(dIntensidad_smoth)  # Ajusta según el valor

  # Vectores de Extremos de la segunda derivada de temperatura
  peaks_max_v=[]
  peaks_min_v=[]

  # Detectar los picos máximos (los minimos de la intenidad)
  peaks_max, properties_max = find_peaks(dIntensidad_smoth, distance=int(distancia), height=umbral_intensidad)

  for i in range(len(peaks_max)):
      peaks_max_v.append(tem_entrada[int(peaks_max[i])])

  # Detectar los picos mínimos (usando la señal negativa)(los maximos de la intensidad)
  peaks_min, properties_min = find_peaks(-dIntensidad_smoth, distance=int(distancia), height=umbral_intensidad)
  for i in range(len(peaks_min)):
      peaks_min_v.append(tem_entrada[int(peaks_min[i])])

  fig, ax1 = plt.subplots()
#___________________________ Graficas ________________________________
  # Graficar la TL original y suavizada en el primer eje Y
  ax1.plot(tem_entrada, intensidad_entrada, 'o', label='Original', alpha=0.3)
  ax1.plot(tem_entrada, intensidad_suavizada, label='Smoothed',color='r' , linewidth=2, alpha=0.5)
  ax1.set_xlabel('Temperature (°C)',fontweight='bold')
  ax1.set_ylabel('TL Intensity ', color='b',fontweight='bold')
  ax1.tick_params(axis='y', labelcolor='b')
  ax1.grid(True)
  # Crear un segundo eje Y para la derivada
  ax2 = ax1.twinx()
  ax2.plot(tem_entrada[:-2], dIntensidad_smoth, label='Derivative', color='g', linestyle='--', alpha=0.6)
  ax2.set_ylabel('Intensity Second Derivative', color='g',fontweight='bold')
  ax2.tick_params(axis='y', labelcolor='g')
  #ax2.grid(True)
  # Marcar los máximos en la gráfica con transparencia
  ax2.plot(peaks_max_v, dIntensidad_smoth[peaks_max], "x", label='Minimums', color='g', alpha=0.9)

  # Marcar los mínimos en la gráfica con transparencia
  ax2.plot(peaks_min_v, dIntensidad_smoth[peaks_min], "o", label='Maximums', color='g', alpha=0.9)

  # Agregar leyenda
  ax1.legend(loc='upper left')  # Leyenda para la intensidad TL
  ax2.legend(loc='upper right')  # Leyenda para la derivada y los picos

  # Mostrar la gráfica
  plt.show()
  I_Resul=[]
  T_Resul=[]
  P_Resul=[]
  for inda, peak_ in enumerate(peaks_min):
      I_ini = intensidad_entrada[peak_]  # Usar la intensidad del pico detectado
      E_ini = 1.0  # Establecer un valor inicial para la energía de activación (ajustarlo según tus datos)
      T_ini = Tabs_entrada[peak_]  # Usar la temperatura del pico detectado
      P_ini = inda+1
      I_Resul.append(I_ini)
      T_Resul.append(T_ini)
      P_Resul.append(P_ini)

  datos = {'Peak':P_Resul,
           'I(a.u)':I_Resul,
           'T (K)':T_Resul,
         }

  df = pd.DataFrame(datos)
  return df

def Deconvolution(DatosEntrada, Parametros_iniciales, lower_bounds, upper_bounds,num_max,rango_min,rango_max,model):
  tem_entrada_0 = DatosEntrada.iloc[:, 0]  # Temperatura en °C
  tem_0 = tem_entrada_0 + 273.15  # Convertir a Kelvin
  intensidad_entrada_0 = DatosEntrada.iloc[:, 1]  # Intensidad
  mask = (tem_entrada_0 >= rango_min) & (tem_entrada_0 <= rango_max)
  tem_entrada = tem_entrada_0[mask].reset_index(drop=True)
  intensidad = intensidad_entrada_0[mask].reset_index(drop=True)
  tem = tem_entrada + 273.15  # Convertir a Kelvin

  #===================== ¡Alerta de datos incorrectos! =========================
  for i, (low, ini) in enumerate(zip(lower_bounds, Parametros_iniciales)):
        if low > ini:
            indice_parametro = i % 4
            nombre_parametro = ['I', 'E', 'T', 'sigma'][indice_parametro]
            num_pico = i // 4 + 1
            raise ValueError(f"Error de límite en el pico {num_pico}: el límite inferior '{nombre_parametro}' es mayor que el valor inicial.")

  for i, (upp, ini) in enumerate(zip(upper_bounds, Parametros_iniciales)):
        if upp < ini:
            indice_parametro = i % 4
            nombre_parametro = ['I', 'E', 'T', 'sigma'][indice_parametro]
            num_pico = i // 4 + 1
            raise ValueError(f"Error de límite en el pico {num_pico}: el límite superior '{nombre_parametro}' es menor que el valor inicial.")



  def modelo(p, x):
    # Inicializa la señal como cero
    y_modelo = np.zeros_like(x)

    # Para cada pico, agregar su contribución al modelo
    num_picos = len(p) // 4  # Cada pico tiene 4 parámetros: I, E, T, sigma
    for i in range(num_picos):
        I = p[4*i]      # Intensidad del i-ésimo pico
        E = p[4*i+1]    # Energía de activación del i-ésimo pico
        T = p[4*i+2]    # Temperatura máxima del i-ésimo pico
        sigma = (p[4*i+3])  # Usar el logaritmo de sigma
        if model[i]=='E':
          y_modelo += DistribucionCTD_Exp(I, E, T, sigma, x)  # Agregar la contribución de cada pico
        else:
          y_modelo += DistribucionCTD_Gaus(I, E, T, sigma, x)  # Agregar la contribución de cada pico

    return y_modelo

  # Definir la función de residuos
  def residuos(p, x, y):
    y_modelo = modelo(p, x)
    return y_modelo - y


  # Realizar el ajuste con restricciones
  res = least_squares(residuos, Parametros_iniciales, method='trf', max_nfev=int(num_max), args=(tem, intensidad), bounds=(lower_bounds, upper_bounds))

  # Obtener el modelo ajustado
  y_modelo_ajustado = modelo(res.x, tem)
  # Sumar intensidades reales y del modelo
  suma_real = np.sum(intensidad)
  suma_modelo_ajustado = np.sum(y_modelo_ajustado)

  # Calcular el FOM
  dx=tem_entrada.iloc[4] - tem_entrada.iloc[3]
  FOM_final = np.sum(np.abs(y_modelo_ajustado-intensidad)) / (suma_real/dx) * 100

  # Mostrar resultados
  Peak_contributions = {}
  num_picos = len(res.x) // 4  # Cada pico tiene tres parámetros: I, E, T
  for i in range(num_picos):
        I = res.x[4*i]      # Intensidad del i-ésimo pico
        E = res.x[4*i+1]    # Energía de activación del i-ésimo pico
        T = res.x[4*i+2]    # Temperatura máxima del i-ésimo pico
        sigma = res.x[4*i+3]  # Sigma del i-ésimo pico
        if model[i]=='E':
          Peak_contributions[f'Peak {i+1}'] = DistribucionCTD_Exp(I, E, T, sigma, tem)
        else:
          Peak_contributions[f'Peak {i+1}'] = DistribucionCTD_Gaus(I, E, T, sigma, tem)

  #-------------------- Histograma--------------------
  residuales = y_modelo_ajustado - intensidad
  # Regla de Sturges para determinar los bins
  n = len(residuales)
  kh = int(1 + np.log2(n))
  # Calcular la media y desviación estándar
  mu, sigma_G = np.mean(residuales), np.std(residuales)

  # Crear un rango de valores para la curva de Gauss
  xG = np.linspace(min(residuales), max(residuales), n)  # Valores entre el mínimo y máximo de los datos
  yG = norm.pdf(xG, mu, sigma_G) * n * (max(residuales) - min(residuales)) / kh  # Ajustar escala al histograma

  frecuencias, bordes = np.histogram(residuales, bins=kh)

  # Crear los bins manualmente
  bins = np.histogram_bin_edges(residuales, bins=kh)

  #------------------------------Graficas----------------------------------
  fig = plt.figure(figsize=(7.5, 10))
  gs = fig.add_gridspec(4, 1, height_ratios=[3, 1, 0.5, 3])  # una fila muy delgada como separador
  # ax1 y ax2 muy pegados
  ax1 = fig.add_subplot(gs[0])
  ax2 = fig.add_subplot(gs[1], sharex=ax1)
  # ax3 justo debajo con un separador pequeño arriba
  ax3 = fig.add_subplot(gs[3])

  # Gráfica principal: modelo ajustado y contribuciones
  ax1.plot(tem_entrada, intensidad, 'x', markersize=4, label='Experimental data')
  ax1.plot(tem_entrada, y_modelo_ajustado, 'r-', label='Final Fitted')
  for i, (peak, contribution) in enumerate(Peak_contributions.items()):
    color = plt.cm.viridis(i / len(Peak_contributions))  # Generar un color único para cada pico
    ax1.plot(tem_entrada, contribution, label=peak, color=color)  # Línea de cada pico
    ax1.fill_between(tem_entrada, contribution, alpha=0.3, color=color)  # Área rellena del mismo color

  ax1.set_ylabel("TL Intensity",fontweight='bold')
  ax1.legend(loc='best')
  ax1.grid(True)
  ax1.set_title(f'FOM: {FOM_final:.4f} %',fontweight='bold')
  ax1.tick_params(labelbottom=False)

  # Segunda gráfica (más pequeña)
  ax2.plot(tem_entrada, residuales, '.', label='Residuals', alpha=0.5)
  ax2.set_xlabel("Temperature (°C)",fontweight='bold')
  ax2.set_ylabel("Residuals",fontweight='bold')
  ax2.grid(True)

  # Graficar histograma

  ax3.hist(residuales, bins=bins, density=False, edgecolor='black', alpha=0.5, label='Residuales', rwidth=0.8)

  # Graficar la curva de Gauss
  ax3.plot(xG, yG, 'r-', linewidth=2, label='Gaussian distribution', alpha=0.5)
  ax3.fill_between(xG, yG, color='r', alpha=0.1)

  # Etiquetas y título
  ax3.set_xlabel('Values range',fontweight='bold')
  ax3.set_ylabel('Frequency',fontweight='bold')
  ax3.set_title(f'Mean={mu:.2f}, Sigma={sigma_G:.2f}',fontweight='bold')
  ax3.legend()
  ax3.grid(True, linestyle='--', alpha=0.6)
  # Cambiar etiquetas del eje X a los rangos
  bin_labels = [f"{bins[i]:.1f} \n {bins[i+1]:.1f}" for i in range(len(bins)-1)]
  ax3.set_xticks(ticks=(bins[:-1] + bins[1:]) / 2, labels=bin_labels, rotation=0)  # Centrar etiquetas y rotarlas
  # Ajustar el espaciado vertical
  plt.subplots_adjust(hspace=0.02, top=0.95, bottom=0.05)
  plt.show()

  #----------------------Tablas----------------------------------------
  #Mostrar los resultados de los parámetros ajustados
  E_result=[]
  T_result=[]
  I_result=[]
  sigma_result=[]
  P_result=[]
  for i in range(num_picos):
    P_result.append(i+1)
    E_result.append(res.x[4*i+1])
    T_result.append(res.x[4*i+2]-273.15)
    I_result.append(res.x[4*i])
    sigma_result.append(res.x[4*i+3])
  datos = {'Peak':P_result,
            'E(eV)':E_result,
           'I(a.u)':I_result,
           'T (°C)':T_result,
           'σ (eV)':sigma_result
         }

  df_resultados = pd.DataFrame(datos)

  # Crear tabla de frecuencias
  tabla_frecuencias = pd.DataFrame({
    'Intervalo': [f"{bordes[i]:.2f} - {bordes[i+1]:.2f}" for i in range(len(bordes)-1)],
    'Frecuencia': frecuencias
  })
  # Crear tabla de la campana de gauss
  tabla_campana = pd.DataFrame({
    'x': xG,
    'y': yG
  })
  tabla_gauss=pd.DataFrame({
      'mu': [mu],
    'sigma': [sigma_G]
  })
  # Mostrar tabla

  tabla_combinada = pd.concat([tabla_frecuencias, tabla_campana, tabla_gauss], axis=1)
  tabla_combinada = tabla_combinada.fillna('')

  return df_resultados, tabla_combinada
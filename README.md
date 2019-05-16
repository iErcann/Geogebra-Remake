## Geogebra-Remake

Ceci est un remake du projet Geogebra en Python.


### Fonctionnalités
 
 
- Affichage de la courbe représentative d'une fonction.
![alt text](https://image.noelshack.com/fichiers/2019/20/4/1558037882-1.png "Logo Title Text 1")

- Création d'un Polygone et calcul de son aire.
![alt text](https://image.noelshack.com/fichiers/2019/20/4/1558038011-2.png "Logo Title Text 1")

- Projection et rotation 3D des points.
![alt text](https://image.noelshack.com/fichiers/2019/20/4/1558038408-3.png "Logo Title Text 1")
![alt text](https://image.noelshack.com/fichiers/2019/20/4/1558038408-4.png "Logo Title Text 1")
![alt text](https://image.noelshack.com/fichiers/2019/20/4/1558038408-5.png "Logo Title Text 1")

- Variable sous forme de curseur modifiable.

 ![alt text](https://image.noelshack.com/fichiers/2019/20/4/1558038505-6.png "Logo Title Text 1")

 
### Controles:
- zqsd: Déplacer le repère
- e/r : Zoom et Dezoom
- ijkl: Test de repère en 3D (inutile)
- c, v, b : Rotation des points dans 3 axes différents
- n : Reset des angles.


### Formalisme des fonctions:
- f(x)=x      <=> f(x)=1*x
- f(x)=sin(x) <=> f(x)=math.sin(1*x)
- f(x)=x²     <=> f(x)=x**2
- f(x)=4x²+3x^3+sin(x)+log(x) <=> f(x)= 4*x**2+3*x**3+math.sin(1*x)+numpy.log(1*x)






 
 


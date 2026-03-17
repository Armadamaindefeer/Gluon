## Modèles

Un modèle permet de spécifié des propriété d'un objet. C'est un fichier .JSON dont La structure est la suivante : 
```json
	{
		"version" : 0,
		"type" : "Basic",
		"alias": [],
		"parent" : [],
		"isCategory": false,
		"properties" : {}
 	}
```
Le nom d'un modèle est le nom du fichier sans extension associé au chemin relatif à la racine de la bibliothèque de modèle.

# Version

La clé version est obligatoire.La version est un nombre entier positif qui augmente à chaque modification non rétrocompatible du lecteur de modèle. Actuellement la version est 0 et le restera jusqu'à la sortie d'une version stable de Gluon

# Type

Les deux valeurs possible sont `Basic` et `Storage`.Cette clé est optionnelle, si elle est absente, la valeur par défaut est soit la valeur indiqué par la catégorie la plus proche en amont du fichier, soit `Basic`.

# Alias

Cette clé est optionnelle et permet de donner des alternative pour le nom du modèle. Ces alternatives viendront remplacer le nom de fichier

# Parent

La clé `parent` est optionnelle et permet de désigner un ou plusieur modèle dont ont doit hériter la structure. L'héritage est n'est pas destructeur, donc si une propriété est déjà fixé par le modèle ou l'un de ses parents, elle ne sera alors pas modifié. Cela signifie que l'ordre des parent est important

# IsCategory

Permet de spécifié un modèle spécial qui définit les propriété de tout les objets présent dans un dossier du même nom et même chemin. Cela définit uniquement les propriété qui ne sont pas encore définie, si jamais un modèle en aval définit une propriété, elle ne sera pas modifié par la catégorie. Cette clé est optionnelle et par défaut la valeur est `false`.

# Properties

Détermine un ensemble de propriété que peut avoir un objet. Ces propriété suivent le formé [here](./datafield.md). 

example : 
```json
	{
		"version" : 0,
		"properties" : {
			"propriété 1" : {"type" : "string"},
			"nombre 1" : {"type" : "int"}
		}
	}
```

# Modèles

Un modèle permet de spécifier les propriétés d'un objet. C'est un fichier json dont la structure est la suivante : 
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
Le nom d'un modèle est le nom sans extension du fichier, associé au chemin relatif depuis la racine de la bibliothèque de modèles.

## version

La clé obligatoire `version` spécifie la version du lecteur de modèle.
La valeur doit être un entier naturel.
Deux versions différentes sont considérées comme incompatibles.
Actuellement, la version est `0` jusqu'à la sortie de la version stable.

## type

La clé optionnelle `type` spécifie le type du modèle.
La valeur doit être `Basic` ou `Storage`.
Par défaut, la valeur est celle indiquée par la catégorie la plus proche en amont du fichier, sinon `Basic`.

## alias

La clé optionnelle `alias` énumère les noms alternatifs du modèle.
La valeur doit être une liste de chaînes de caractères.

## parent

La clé optionnelle `parent` identifie les modèles dont ce modèle hérite la structure.
Lors du chargement des modèles, si une propriété est déjà définie par le modèle ou par un parent traité en amont, elle ne sera alors pas modifiée.
La valeur doit être une liste de chaînes de caractères.

## isCategory

La clé optionnelle `isCategory` détermine si les propriétés du modèle se répercutent sur l'ensemble des modèles présents dans le dossier homonyme situé au même emplacement. 
Seules les propriétés qui ne sont pas définies dans les modèles de ce dossier seront ajoutées.
La valeur doit être un booléen. Par défaut, la valeur est `false`.

## properties

La clé optionnelle `properties` répertorie l'ensemble des propriétés du modèle.
La valeur doit suivre le format de définition des [datafields](./datafield.md). 

Exemple : 
```json
	{
		"version" : 0,
		"properties" : {
			"propriete_1" : {"type" : "string"},
			"nombre_1" : {"type" : "int"}
		}
	}
```

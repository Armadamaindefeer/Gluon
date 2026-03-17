## Datafield

Un Datafield est un dictionnaire Json permettant de décrire la valeur d'une entrée

La forme générale d'un datafield est:
```json
	{
		"type" : <string>,
		"allowNone" : <bool>,
		"default" : <str:bool:float:int>,
		"selectValue" : <list>
	}
```
Chacune de ces propriétés,mis à part "type", sont optionnelle. Cependant si une clé non présente dans cette liste est écrite dans un datafield, alors il sera jugé malformé et sera rejeté.

# Type
Il existe 5 types différents : 
	- "string" : Chaîne de caractère, encodée en UTF-8
	- "bool" : booléan
	- "float" : nombre à virgule flottante
	- "int" : nombre entier
	- "comment" : commentaire, à savoire que si un datafield possède ce type il sera totalement ignoré

# Default

Donne la valeur par défaut d'un datafield qui peut être utilisé en cas d'erreur ou juste de mise à défaut. Il peut prendre deux type différent : soit le type indiqué dans `type` soit `None`.

# AllowNone

Détermine si la valeur spécial `None`, `null` ou équivalent, est autorisée. Si `allowNone` est à `False` et que `default` est à `None` alors le datafield est invalidé.

# SelectValue

Permet de restreindre les valeurs possible d'un datafield à un ensemble prédéfini de valeur. Ces valeurs sont prévu pour être choisi par un utilisateur. Si jamais la clé `default` est présente, alors la valeur spécifié est aussi valide mais ne dois pas être selectionnable par l'utilisateur

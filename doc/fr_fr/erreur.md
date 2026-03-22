# Erreur d'index


|N° | Nom						| Description											|
|---|---------------------------|-------------------------------------------------------|
|1  | INVALID_ARGUMENT			| Le paramètre spécifié à la commande est invalide		|
|2  | INVALID_LOCAL_INDEX		| L'index local est invalide, soit trop grand, trop petit ou le nombre n'est pas entier |
|3  | INVALID_SELECTED_INDEX	| L'index de selection est invalide, soit trop grand, trop petit ou le nombre n'est pas entier |
|4  | INVALID_UUID				| L'UUID fournit n'existe pas |
|5  | UNEXPECTED				| Erreur inattendu |

# Erreur serveur

|N° |
|---|-----------------------|----------------------------------------------------------|
|1	|MODIFIYING_UNIVERSE	| Une operation modifierait l'univers
|2	|CREATING_UNIVERSE		| Il ne peut y avoir qu'un seul univers
|3	|HAS_PARENT				| On objet doit d'abord être déstocké avant d'être stocké
|4	|ALREADY_STORED			| Un objet est déjà présent dans un stockage
|5	|NOT_STORED				| 
|6	|NOT_A_STORAGE			| Un objet n'est pas un stockage
|7	|NOT_EMPTY				|
|8	|STACKED_STORAGE		|
|9	|SAME_OBJECT			|
|10	|UNEXPECTED				|
|11	|DOES_NOT_EXIST			|
|12	|JSON_DECODER_ERROR		|
|13	|VERSION_OUTDATED		|
|14	|UNKNOWN_VERSION		|
|15	|MALFORMED_PARENT		|
|16	|MALFORMED_TYPE			|
|17	|MALFORMED_PROPERTY		|
|18	|MALFORMED_ALIAS		|
|19	|MALFORMED_ISCATEGORY	|
|20	|MALFORMED_DATABASE		|
|21	|UNEXISTANT_FILE		|
|22	|OVERCONSUMPTION		| Une operation consommerait plus

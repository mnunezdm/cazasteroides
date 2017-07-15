(function(window, undefined) {
  var dictionary = {
    "7a8ab4e3-a652-419e-b213-9dccf6672ba7": "Splash Screen",
    "df46f12d-8d34-415f-878c-8f34073eb6d4": "NuevaObservacion",
    "9d0b23f0-e3f1-4389-8618-affa0c690df4": "Ayuda",
    "ca3704e6-7bdd-4f38-a2f2-7d45fd0748d2": "ObservacionDetallada",
    "72d4950b-d705-4f69-9a03-f83d045e4bd4": "Stats",
    "70309ff9-384f-48d8-8ae4-e0975cc4ecc3": "AcercaDe",
    "66c252c8-1e7c-4aee-a828-bf951def0367": "Home",
    "faf9e1c9-92cb-461e-a49f-89735101eed5": "Login",
    "e89e3cab-b952-46d2-8888-56c05c9f4343": "EditarPerfil",
    "ea522a0d-ae45-4a39-af62-9f8c22ff8269": "Register",
    "c05fdd39-8da5-4c07-b36b-ebd91ce0a3e4": "CargandoObservacion",
    "b9dc3b40-498f-45ba-8244-13a459d6cc74": "ScreenWithBack",
    "ab8d3f52-7dd3-4b2e-9631-8e0ee6945232": "StatusAndNavbar",
    "67b92904-8878-4926-a40e-8d7723101a04": "EmptyScreen",
    "bb8abf58-f55e-472d-af05-a7d1bb0cc014": "default"
  };

  var uriRE = /^(\/#)?(screens|templates|masters|scenarios)\/(.*)(\.html)?/;
  window.lookUpURL = function(fragment) {
    var matches = uriRE.exec(fragment || "") || [],
        folder = matches[2] || "",
        canvas = matches[3] || "",
        name, url;
    if(dictionary.hasOwnProperty(canvas)) { /* search by name */
      url = folder + "/" + canvas;
    }
    return url;
  };

  window.lookUpName = function(fragment) {
    var matches = uriRE.exec(fragment || "") || [],
        folder = matches[2] || "",
        canvas = matches[3] || "",
        name, canvasName;
    if(dictionary.hasOwnProperty(canvas)) { /* search by name */
      canvasName = dictionary[canvas];
    }
    return canvasName;
  };
})(window);
import React, { useContext } from "react";
import { ListList, ListItem, List } from "semantic-ui-react";
import { DataContext } from "../context/DataContext";

export const Instructions = (props) => {
    const { data, setData } = useContext(DataContext);

    const renderCategoryList = () => {
        return (
            <>
              {data.categories.map((c, i) => {
                return (
                    <ListItem key={i} style={{ width: "25%" }}>
                        {c}
                    </ListItem>
                );
              })}
            </>
          );
      };

    return (
        <section id="instructions" style={{ padding: "25px" }}>
            <h1>Instrucciones</h1>
            <p style={{ textAlign: "justify" }}>
                A la derecha encontrarás una frase describiendo una entidad visual, deberás escoger en el menú desplegable cuál de las categorías semánticas de la lista describe mejor el sujeto de la oración. Puedes considerar sinónimos (p. ej., “automóvil” en lugar de carro), hipónimos (p. ej., “sedán” como un tipo de carro) o merónimos (p. ej., “rueda” como parte de una bicicleta) para identificar el concepto subyacente. En caso de que este no encaje con ninguna de las 19 categorías listadas deberás seleccionar “None of the above”. La lista de categorías semánticas posibles es la siguiente:
            </p>
            <List bulleted horizontal>
                <p></p>
                {renderCategoryList()}
            </List>
            <p style={{ textAlign: "justify" }}>A continuación, puedes encontrar ejemplos de las categorías que se deben asignar a algunas descripciones:</p>
            <List>
                <ListItem>“Red car stopped at a traffic light” - car</ListItem>
                <ListItem>“Sky with scattered clouds” - sky</ListItem>
                <ListItem>“Pedestrian standing next to a bus” - person</ListItem>
                <ListItem>“Graffiti on the wall of an old building” - wall</ListItem>
                <ListItem>“Person riding a motorcycle on the sidewalk” - rider</ListItem>
                <ListItem>“Corgi playing with a ball” - None of the above</ListItem>
            </List>
            <p style={{ textAlign: "justify" }}>Por último, ten en cuenta las siguientes consideraciones:</p>
            <List ordered>
                <ListItem>Si se mencionan varios objetos, elige solo la categoría más relevante.</ListItem>
                <ListItem>Si la descripción no se ajusta a ninguna de las categorías, selecciona "None of the above".</ListItem>
                <ListItem>Si tienes dudas, pregúntate:
                    <ListList>
                        <ListItem as='li'  value='-'>¿Qué objeto o entidad es el sujeto de la descripción?</ListItem>
                        <ListItem as='li' value='-'>¿Qué categoría semántica describe mejor ese objeto o entidad?</ListItem>
                        <ListItem as='li' value='-'>¿Se menciona explícitamente alguna de las categorías listadas?</ListItem>
                    </ListList>
                </ListItem>
            </List>
        </section>
    );
};

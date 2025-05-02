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
            <h1>Instructions</h1>
            <p style={{ textAlign: "justify" }}>
                On the right, you will see a sentence describing a visual entity (such as an object, animal, body part, etc.). You must select from the dropdown menu the semantic category from the list that best describes the subject of the sentence. The list of possible semantic categories is as follows:
            </p>
            <List bulleted horizontal>
                <p></p>
                {renderCategoryList()}
            </List>
            <p style={{ textAlign: "justify" }}>The subject described may not always match the categories exactly, so you should choose the category that most closely corresponds to it. You may consider synonyms (e.g., if the subject is "automobile", select car), hyponyms (e.g., if the subject is "sedan", select car, since it is a type of car), or meronyms (e.g., if the subject is “wheel” and it is part of a bicycle, select bicycle) to identify the underlying concept. If the subject does not fit any of the 19 listed categories, select “None of the above”.
            </p>
            <p style={{ textAlign: "justify" }}>Below are some examples of how categories should be assigned to different descriptions:
            </p>
            <List>
                <ListItem>“Red car stopped at a traffic light” - car</ListItem>
                <ListItem>“Sky with scattered clouds” - sky</ListItem>
                <ListItem>“Pedestrian standing next to a bus” - person</ListItem>
                <ListItem>“Graffiti on the wall of an old building” - wall</ListItem>
                <ListItem>“Person riding a motorcycle on the sidewalk” - rider</ListItem>
                <ListItem>“Corgi playing with a ball” - None of the above</ListItem>
            </List>
            <p style={{ textAlign: "justify" }}>Finally, keep the following considerations in mind:
            </p>
            <List ordered>
                <ListItem>If multiple objects are mentioned, select only the most relevant category.</ListItem>
                <ListItem>If the description does not match any category, select "None of the above."</ListItem>
                <ListItem>If you're unsure, ask yourself:
                    <ListList>
                        <ListItem as='li'  value='-'>What object or entity is the subject of the description?</ListItem>
                        <ListItem as='li' value='-'>Which semantic category best describes that object or entity?</ListItem>
                        <ListItem as='li' value='-'>Is any of the listed categories explicitly mentioned?</ListItem>
                    </ListList>
                </ListItem>
            </List>
        </section>
    );
};

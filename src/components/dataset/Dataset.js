import React, { useEffect, useState } from "react";
import { Container, Segment, Grid } from "semantic-ui-react";

import { DataContext } from "../context/DataContext";
import { Caption } from "./Caption";
import { Instructions } from "./Instructions";

export const Dataset = (props) => {
    const [data, setData] = useState({
        method: "ours",
        id: 0,
        description: "",
        category: "",
        categories: ["road", "sidewalk","building","wall","fence","pole","traffic light","traffic sign","vegetation","terrain","sky","person","rider","car","truck","bus","train","motorcycle","bicycle", "None of the above"],
    });

    const fetchData = () => {
        let method = data.method === "ours" ? "osprey" : "ours";
        fetch(
        `https://lambda004.uniandes.edu.co/api/${method}/ids`
        ).then((response) => {
        response.json().then((ids) => {
            let id = ids[(Math.random() * ids.length) | 0].id;
            fetch(
            `https://lambda004.uniandes.edu.co/api/${method}/${id}`
            ).then((response) => {
                response.json().then((item) => {
                let description = item.description;
                setData({
                    ...data,
                    method: method,
                    id: id,
                    description: description,
                    categories: data.categories,
                });
            });
            });
        });
        });
    };


    const postData = (category) => {
        fetch(`https://lambda004.uniandes.edu.co/api/${data.method}/${data.id}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ category }),
        })
            .then((response) => {
            if (!response.ok) {
                console.error("Error en la respuesta del servidor:", response);
                throw new Error("Error al enviar los datos");
            }
            return response.json();
            })
            .then((result) => {
                fetchData();
            })
            .catch((error) => {
                console.error("Error en la solicitud POST:", error);
            });
    };


    useEffect(() => {
        fetchData();
    }, []);

    return (
        <DataContext.Provider value={{ data, setData }}>
        <Segment id="dataset" vertical padded="very">
            <Container textAlign="center">
            <Grid columns="equal" celled="internally" stackable>
                <Grid.Row>
                <Grid.Column textAlign="left" padded="10px">
                    <Instructions categories={data.categories}/>
                </Grid.Column>
                <Grid.Column textAlign="center">
                    <Caption categories={data.categories} description={data.description} fetchData={fetchData} postData={postData}/>
                </Grid.Column>
                </Grid.Row>
            </Grid>
            </Container>
        </Segment>
        </DataContext.Provider>
    );
};

import React, { useState, useEffect, useContext } from "react";
import { Grid, Button, Icon, FormSelect,
    FormGroup,
    Form, } from "semantic-ui-react";

import { DataContext } from "../context/DataContext";

export const Caption = (props) => {
  const { data, setData } = useContext(DataContext);

  const [state, setState] = useState({
    id: 0,
    description: "",
    category: "",
    categories: [],
  });

  useEffect(() => {
    if (data.categories && data.categories.length > 0) {
      const categories = data.categories.map((category, index) => ({
        key: index,
        value: category.value || category, 
        text: category.text || category,
      }));
      setState({
        ...state,
        id: data.id,
        description: data.description,
        categories: categories,
      });
    }
  }, [data.description, data.categories]);

  const handleNext = () => {
    props.postData(state.category);
    setState({ ...state, category: "" });
  };

  return (
    <Grid id="caption" stackable style={{ padding: "25px" }}>
      <Grid.Row style={{ textAlign: "center", padding: "10px" }}>
        <Grid.Column textAlign="left">
            <p>"{state.description}"</p>
        </Grid.Column>
      </Grid.Row>
      <Grid.Row>
        <Grid.Column textAlign="center">
        <Form>
            <p style={{ textAlign: "justify" }}>
                Select the semantic category that best describes the subject of the sentence:
            </p>
            <FormGroup widths='equal'>
            <FormSelect
                fluid
                value={state.category}
                onChange={(e, { value }) => {
                    setState({ ...state, category: value });
                }}
                options={state.categories}
                placeholder='category'
            />
            </FormGroup>
        </Form>
        </Grid.Column>
      </Grid.Row>
      <Grid.Row>
        <Grid.Column textAlign="right">
          <Button icon labelPosition="right" secondary onClick={handleNext} disabled={state.category === ""}>
            Next
            <Icon name="right arrow" />
          </Button>
        </Grid.Column>
      </Grid.Row>
    </Grid>
  );
};

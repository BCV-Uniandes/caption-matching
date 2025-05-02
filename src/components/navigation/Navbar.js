import React from "react";
import { Container, Menu, Segment, Visibility } from "semantic-ui-react";

export const Navbar = (props) => {
  return (
    <Visibility
      once={true}
    >
      <Segment inverted vertical>
        <Menu
          fixed="top"
          inverted
          pointing
          secondary
          style={{ backgroundColor: "black", padding: "1em" }}
        >
          <Container inverted>
          </Container>
        </Menu>
      </Segment>
    </Visibility>
  );
};

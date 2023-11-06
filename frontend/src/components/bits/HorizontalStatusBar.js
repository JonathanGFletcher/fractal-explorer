import React from "react";
import styled from "styled-components";

const HorizontalStatusBar = ({ percentage = 0 }) => {
	return (
		<>
			<Container>
				<Bar>
					<Progress style={{ width: `${percentage}%` }}></Progress>
				</Bar>
			</Container>
		</>
	);
};

const Container = styled.div`
	width: 100%;
	height: 2vw;
	padding: 3px 0;
`;

const Bar = styled.div`
	width: 100%;
	height: 100%;
	background-color: #333;
	border-radius: 500px;
	overflow: hidden;
`;

const Progress = styled.div`
	height: 100%;
	background-color: #f37878;
	border-radius: 500px;
`;

export default HorizontalStatusBar;

import React, { useEffect } from "react";
import { useFractalContext } from "../contexts/FractalContext";
import styled from "styled-components";
import * as NetworkService from "../services/NetworkService";

const FullViewFractal = () => {

    const FractalContext = useFractalContext();
    const params = FractalContext.fullViewParams;

    const tilesX = 4;
    const tilesY = 4;
    
    useEffect(() => {
        if (params != null) {
            console.log(params);
        }
    }, [params]);

    return <Container>

    </Container>
}

const Container = styled.div`
    position: relative;
    width: 100%;
    height: 100%;
`;

export default FullViewFractal;
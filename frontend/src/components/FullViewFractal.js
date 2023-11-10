import React, { useState, useEffect } from "react";
import { useFractalContext, useFractalUpdateContext } from "../contexts/FractalContext";
import styled from "styled-components";
import * as NetworkService from "../services/NetworkService";

const FullViewFractal = () => {

    const FractalContext = useFractalContext();
    const params = FractalContext?.fullViewParams;

    const FractalUpdateContext = useFractalUpdateContext();
    const updateFullViewParams = FractalUpdateContext?.updateFullViewParams;

    const tilesX = 5;
    const tilesY = 4;

    const { innerWidth, innerHeight } = window;
    const fullImageWidth = innerWidth - 20;
    const fullImageHeight = innerHeight - 20;
    const chunkWidth = fullImageWidth / tilesX;
    const chunkHeight = fullImageHeight / tilesY;

    const tiles = Array.from(
        Array(tilesX), (_, x) => 
            Array.from(
                Array(tilesY), (_, y) => {
                    return {
                        x: x,
                        y: y,
                    }
                }
            )
    );

    console.log(tiles);

    return <Container>
        <FractalContainer>

            { tiles.map(row => 
                <FractalRow>

                    { row.map(c => 
                        <FractalChunk>
                            <FractalImage 
                            x={ c.x } y={ c.y } 
                            tilesX={ tilesX } tilesY={ tilesY } 
                            chunkWidth={ chunkWidth } chunkHeight={ chunkHeight } 
                            params={ params } 
                            />
                        </FractalChunk>
                    ) }

                </FractalRow>
            ) }
            
        </FractalContainer>
    </Container>
}

const Container = styled.div`
    position: relative;
    width: 100%;
    height: 100%;
    padding: 10px;
`;

const FractalContainer = styled.div`
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
`;

const FractalRow = styled.div`
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
`;

const FractalChunk = styled.div`
    position: relative;
    width: 100%;
    height: 100%;
`;



const FractalImage = ({ x, y, tilesX, tilesY, chunkWidth, chunkHeight, params }) => {
    if (params == null) {
        return <FractalBackground>
            <FractalBackgroundPlaceholder />
        </FractalBackground>
    }

    const width = params?.dimensions?.width / tilesX;
    const height = params?.dimensions?.height / tilesY;

    const minX = width * x;
    const minY = height * y; //params?.dimensions?.height - (height * y + height);
    const maxX = width * x + width - 1;
    const maxY = height * y + height - 1; //params?.dimensions?.height - (height * y) - 1;

    const reqParams = {
        ...params,
        dimensions: {
            ...params?.dimensions,
            view_min_x: minX,
            view_min_y: minY,
            view_max_x: maxX,
            view_max_y: maxY,
        }
    };

    const [imageUrl, setImageUrl] = useState(null);

    useEffect(() => {
        NetworkService.getFractal(reqParams)
        .then(data => setImageUrl(data?.url))
        .catch(e => alert(e));
    })

    return <FractalImageContainer>
        { imageUrl == null ?
            <FractalBackground>
                <FractalBackgroundPlaceholder />
            </FractalBackground>
            :
            <img src={ imageUrl } style={{ position: 'relative', width: chunkWidth, height: chunkHeight }} />
        }
    </FractalImageContainer>
}

const FractalImageContainer = styled.div`
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    overflow: hidden;
`;

const FractalBackground = styled.div`
    position: relative;
    width: 100%;
    height: 100%;
    padding: 5px;
`;

const FractalBackgroundPlaceholder = styled.div`
    position: relative;
    width: 100%;
    height: 100%;
    background-color: #262626;
    border-radius: 5px;
`;

// width: 25vw;
// height: 25vh;
// object-fit: fill;



export default FullViewFractal;
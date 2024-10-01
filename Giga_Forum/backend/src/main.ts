import { NestFactory } from '@nestjs/core'
import { AppModule } from './app.module'
import { ValidationPipe } from './pipes/validation.pipe';
import cors from 'cors'

async function start() {
    const PORT = process.env.PORT || 5000;

    const app = await NestFactory.create(AppModule, { cors: true });
    
    app.useGlobalPipes(new ValidationPipe());
    // app.use(cors());

    await app.listen(PORT, () => {
        console.log(`server started in ${PORT}`);
    });
}

start();

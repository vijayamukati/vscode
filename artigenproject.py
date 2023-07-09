import tensorflow as tf
from tensorflow.keras import layers

# Generator Network
def build_generator(latent_dim):
    model = tf.keras.Sequential()
    model.add(layers.Dense(256, input_dim=latent_dim))
    model.add(layers.LeakyReLU(alpha=0.2))
    model.add(layers.Dense(512))
    model.add(layers.LeakyReLU(alpha=0.2))
    model.add(layers.Dense(1024))
    model.add(layers.LeakyReLU(alpha=0.2))
    model.add(layers.Dense(784, activation='tanh'))
    model.add(layers.Reshape((28, 28, 1)))
    return model

# Discriminator Network
def build_discriminator():
    model = tf.keras.Sequential()
    model.add(layers.Flatten(input_shape=(28, 28, 1)))
    model.add(layers.Dense(512))
    model.add(layers.LeakyReLU(alpha=0.2))
    model.add(layers.Dense(256))
    model.add(layers.LeakyReLU(alpha=0.2))
    model.add(layers.Dense(1, activation='sigmoid'))
    return model

# GAN Model
def build_gan(generator, discriminator):
    discriminator.trainable = False
    model = tf.keras.Sequential()
    model.add(generator)
    model.add(discriminator)
    return model

# Training Loop
def train_gan(gan, discriminator, generator, dataset, latent_dim, epochs, batch_size):
    discriminator.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=0.0002, beta_1=0.5))
    gan.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=0.0002, beta_1=0.5))
    
    for epoch in range(epochs):
        for batch in dataset:
            # Train Discriminator
            noise = tf.random.normal(shape=(batch_size, latent_dim))
            generated_images = generator.predict(noise)
            real_images = batch
            x = tf.concat([real_images, generated_images], axis=0)
            y = tf.concat([tf.ones((batch_size, 1)), tf.zeros((batch_size, 1))], axis=0)
            discriminator_loss = discriminator.train_on_batch(x, y)
            
            # Train Generator
            noise = tf.random.normal(shape=(batch_size, latent_dim))
            y = tf.ones((batch_size, 1))
            generator_loss = gan.train_on_batch(noise, y)
            
        print(f"Epoch {epoch+1}/{epochs} - D Loss: {discriminator_loss} - G Loss: {generator_loss}")
        
# Load and preprocess the dataset
(train_images, _), (_, _) = tf.keras.datasets.mnist.load_data()
train_images = train_images.reshape(train_images.shape[0], 28, 28, 1).astype('float32')
train_images = (train_images - 127.5) / 127.5
buffer_size = train_images.shape[0]
batch_size = 128  # Modified batch size
train_dataset = tf.data.Dataset.from_tensor_slices(train_images).shuffle(buffer_size).batch(batch_size)

# Load and preprocess the dataset
(train_images, _), (_, _) = tf.keras.datasets.mnist.load_data()
train_images = train_images.reshape(train_images.shape[0], 28, 28, 1).astype('float32')
train_images = (train_images - 127.5) / 127.5
buffer_size = train_images.shape[0]
batch_size = 256  # Modified batch size (divisible by dataset size)
train_dataset = tf.data.Dataset.from_tensor_slices(train_images).shuffle(buffer_size).batch(batch_size)

# Example Usage
latent_dim = 100
generator = build_generator(latent_dim)
discriminator = build_discriminator()
gan = build_gan(generator, discriminator)

# Compile the Discriminator and GAN models
discriminator.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=0.0002, beta_1=0.5))
gan.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=0.0002, beta_1=0.5))

# Train the GAN
epochs = 100
train_gan(gan, discriminator, generator, train_dataset, latent_dim, epochs, batch_size)

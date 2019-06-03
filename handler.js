export const hello = async (event, context) => {
  try {
    return {
      statusCode: 200,
      body: JSON.stringify({
        message: `Go Serverless v1.0! ${(await message({ time: 1, copy: 'Your function executed successfully!'}))}`,
      }),
    };
  }
  catch(e) {
    console.log(e);
    failure({status: false});
  }
};

const message = ({ time, ...rest }) => new Promise((resolve, reject) =>
  setTimeout(() => {
    resolve(`${rest.copy} (with a delay)`);
  }, time * 1000)
);
